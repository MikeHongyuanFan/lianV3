/**
 * WebSocket Service
 * Handles WebSocket connections for real-time notifications
 */
import { useAuthStore } from '../store/auth';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectTimeout = null;
    this.reconnectInterval = 3000; // 3 seconds
    this.subscribers = {};
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
    // Extract the base URL without the '/api' path if it exists
    const baseUrlWithoutApi = this.baseUrl.replace(/\/api$/, '');
    // According to the WebSockets implementation in AmazonQ.md, the correct path is /ws/notifications/
    this.wsUrl = baseUrlWithoutApi.replace(/^http/, 'ws') + '/ws/notifications/';
  }

  /**
   * Connect to the WebSocket server
   * @returns {Promise} Promise that resolves when connected
   */
  connect() {
    return new Promise((resolve, reject) => {
      if (this.isConnected) {
        resolve();
        return;
      }

      const authStore = useAuthStore();
      const token = authStore.accessToken;

      if (!token) {
        console.log('No authentication token available, will try to connect later');
        reject(new Error('No authentication token available'));
        return;
      }

      // Close existing socket if any
      if (this.socket) {
        this.socket.close();
        this.socket = null;
      }

      try {
        // Create WebSocket connection with JWT token
        const wsUrl = `${this.wsUrl}?token=${token}`;
        console.log('Connecting to WebSocket URL:', wsUrl);
        
        // Add a small delay before creating the WebSocket to avoid race conditions
        setTimeout(() => {
          try {
            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
              console.log('WebSocket connected');
              this.isConnected = true;
              this.reconnectAttempts = 0;
              resolve();
            };

            this.socket.onclose = (event) => {
              console.log('WebSocket disconnected', event);
              this.isConnected = false;
              this._attemptReconnect();
            };

            this.socket.onerror = (error) => {
              console.error('WebSocket error:', error);
              this.isConnected = false;
              reject(error);
            };

            this.socket.onmessage = (event) => {
              try {
                const data = JSON.parse(event.data);
                this._handleMessage(data);
              } catch (error) {
                console.error('Error parsing WebSocket message:', error, 'Raw message:', event.data);
              }
            };
          } catch (innerError) {
            console.error('Error creating WebSocket connection:', innerError);
            reject(innerError);
          }
        }, 100);
      } catch (error) {
        console.error('Error creating WebSocket:', error);
        reject(error);
      }
    });
  }

  /**
   * Disconnect from the WebSocket server
   */
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    
    this.isConnected = false;
    
    // Clear any pending reconnect attempts
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
  }

  /**
   * Send a message to the WebSocket server
   * @param {Object} message - Message to send
   */
  send(message) {
    if (!this.isConnected) {
      console.error('Cannot send message, WebSocket not connected');
      return;
    }

    this.socket.send(JSON.stringify(message));
  }

  /**
   * Subscribe to a specific message type
   * @param {string} type - Message type to subscribe to
   * @param {Function} callback - Callback function to execute when message is received
   * @returns {Function} Unsubscribe function
   */
  subscribe(type, callback) {
    if (!this.subscribers[type]) {
      this.subscribers[type] = [];
    }

    this.subscribers[type].push(callback);

    // Return unsubscribe function
    return () => {
      if (this.subscribers[type]) {
        this.subscribers[type] = this.subscribers[type].filter(cb => cb !== callback);
      }
    };
  }

  /**
   * Attempt to reconnect to the WebSocket server
   * @private
   */
  _attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log('Max reconnect attempts reached');
      return;
    }

    this.reconnectAttempts++;
    console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);

    this.reconnectTimeout = setTimeout(() => {
      this.connect().catch(error => {
        console.error('Reconnect failed:', error);
      });
    }, this.reconnectInterval * Math.min(this.reconnectAttempts, 3)); // Cap the backoff at 3x the base interval
  }

  /**
   * Handle incoming WebSocket messages
   * @param {Object} data - Message data
   * @private
   */
  _handleMessage(data) {
    console.log('WebSocket message received:', data);
    
    // Ensure data has the expected structure
    if (!data || typeof data !== 'object') {
      console.error('Invalid WebSocket message format:', data);
      return;
    }
    
    const type = data.type || 'unknown';
    
    // Handle different message formats
    // Some backends send payload in a 'payload' field, others send it directly in the message
    let payload = data.payload;
    
    // If payload is undefined but there are other properties that might be the payload,
    // pass the entire data object as the payload
    if (payload === undefined && Object.keys(data).length > 1) {
      // Create a copy of data without the type field to use as payload
      const { type: _, ...rest } = data;
      payload = Object.keys(rest).length > 0 ? rest : undefined;
    }

    // Notify all subscribers for this message type
    if (this.subscribers[type]) {
      this.subscribers[type].forEach(callback => {
        try {
          callback(payload);
        } catch (error) {
          console.error(`Error in subscriber callback for type "${type}":`, error);
        }
      });
    }

    // Notify all subscribers for 'all' messages
    if (this.subscribers['all']) {
      this.subscribers['all'].forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Error in subscriber callback for "all":', error);
        }
      });
    }
  }
}

// Create singleton instance
const websocketService = new WebSocketService();

export default websocketService;
