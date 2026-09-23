## Tables

| Requirement   | SPEC / AC     |  Task   |  Files                                                    |  Test                                    |  Status  | 
| ------------- |:-------------:|:-------:|:---------------------------------------------------------:|:----------------------------------------:|:--------:|
| FR-01         | AC-01         | T-03    |src/services/search_service.py                             |test_search_service.py                    |  Passed  |
| FR-02         | AC-02         | T-03    |src/services/search_service.py                             |test_search_service.py                    |  Passed  |
| FR-03         | AC-03         | T-04    |src/domain/exceptions.py, src/services/search_service.py   |tests/unit/test_validation.py             |  Passed  |
| FR-04         | AC-04         | T-03    |src/services/search_service.py                             |test_search_service.py                    |  Passed  |
| FR-05         | AC-04         | T-03    |src/services/search_service.py                             |test_search_service.py                    |  Passed  |
| FR-06         | AC-03         | T-04    |src/domain/exceptions.py, src/services/search_service.py   |tests/unit/test_validation.py             |  Passed  |
| NFR-01        | AC-05         | T-02    |src/domain/models.py, src/repository/customer_repository.py|tests/unit/test_models.py                 |  Passed  |
| NFR-02        | AC-06         | T-06    |tests/, .coveragerc                                        |pytest --cov=src --cov-report=term-missing|  Passed  |
| NFR-03        | -----         | T-05    |src/entrypoints/cli.py                                     |tests/integration/test_interface.py       |  Passed  |