# 🧪 Test Coverage Report

## 📄 Summary

- Total test files found: **60**
- Successful tests: **29**
- Failed tests: **31**

## ❌ Failed Tests

- tests/unit/consumers/test_notification_consumer.py
- tests/unit/filters/test_advanced_filters.py
- tests/unit/filters/test_notification_filter.py
- tests/unit/services/test_application_service.py
- tests/unit/services/test_auth_service.py
- tests/unit/services/test_document_services.py
- tests/unit/services/test_user_notification_service.py
- tests/unit/tasks/test_celery_base.py
- tests/unit/tasks/test_celery_config.py
- tests/unit/tasks/test_mock_tasks.py
- tests/unit/tasks/test_task_error_handling.py
- tests/unit/tasks/test_task_execution.py
- tests/unit/tasks/test_task_execution_simplified.py
- tests/unit/tasks/test_task_factories.py
- tests/unit/tasks/test_task_integration.py
- tests/unit/tasks/test_task_scheduling.py
- tests/unit/test_application_serializers.py
- tests/unit/test_application_services.py
- tests/unit/test_application_views.py
- tests/unit/test_borrower_views.py
- tests/unit/test_document_serializers.py
- tests/unit/test_document_services.py
- tests/unit/test_edge_cases.py
- tests/unit/test_notification_services.py
- tests/unit/test_websocket_api.py
- tests/unit/test_websocket_auth.py
- tests/unit/test_websocket_consumers.py
- tests/unit/websocket/test_consumers.py
- tests/unit/websocket/test_notification_websocket.py
- tests/unit/websocket/test_websocket_auth.py
- tests/unit/websocket/test_websocket_connection.py

## 📈 Module Coverage Overview
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
applications/filters.py                     17      0   100%
applications/models.py                      85      1    99%
applications/serializers.py                184     54    71%
applications/services.py                    51     51     0%
applications/services_extended.py          123     13    89%
applications/services_impl.py              100      1    99%
applications/tasks.py                       65      0   100%
applications/validators.py                  79     74     6%
applications/views.py                      240     91    62%
borrowers/filters.py                        16      0   100%
borrowers/models.py                         82      0   100%
borrowers/serializers.py                    39      2    95%
borrowers/services.py                       51      0   100%
borrowers/urls_guarantors.py                 6      0   100%
borrowers/views.py                          88     15    83%
brokers/filters.py                          27      4    85%
brokers/models.py                           44      0   100%
brokers/serializers.py                      47     11    77%
brokers/views.py                           111     63    43%
crm_backend/celery.py                        8      0   100%
crm_backend/settings_integration.py         16     16     0%
documents/filters.py                        39      1    97%
documents/models.py                         93      3    97%
documents/serializers.py                    81     10    88%
documents/services.py                       46     40    13%
documents/services_mock.py                  40      0   100%
documents/signals.py                        16      0   100%
documents/views.py                         189     37    80%
reports/models.py                            1      0   100%
reports/serializers.py                      30      0   100%
reports/views.py                           116     13    89%
run_all_tests_with_coverage.py              58     58     0%
run_test_files.py                          123    123     0%
users/consumers.py                          32     32     0%
users/filters.py                            14      0   100%
users/models.py                             58      0   100%
users/permissions.py                        19      7    63%
users/routing.py                             3      3     0%
users/serializers.py                        50      3    94%
users/services.py                           60     60     0%
users/services/auth_service.py              27      2    93%
users/services/notification_service.py      59      6    90%
users/views.py                             163     40    75%
------------------------------------------------------------
TOTAL                                     2796    834    70%