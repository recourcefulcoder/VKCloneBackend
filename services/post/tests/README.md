# Testing documentation
This README file contains some crucial for test support notes (so-called "documentation")


## Patching in tests
Patching is evil, yet here it seemed impossible to avoid

Tests, in order not to set up actual users service for testing validation, 
implemented mocking of httpx.AsyncClient.get method - SO 

If one day logic of authentication will change (meaning requests, sent to user service 
will be made in any other way but with httpx.AsyncClient's get() method) these patched 
tests will fail will require rewriting

