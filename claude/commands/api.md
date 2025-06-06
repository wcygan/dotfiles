Generate API endpoint for $ARGUMENTS.

Steps:
1. Analyze project structure and frameworks:
   - Detect web framework (Express, FastAPI, Spring, Gin, etc.)
   - Identify existing API patterns and conventions
   - Check authentication/authorization methods
   - Review API versioning strategy
   - Understand request/response formats (JSON, protobuf, etc.)

2. Design endpoint:
   - Determine HTTP method (GET, POST, PUT, DELETE, PATCH)
   - Design RESTful URL path following conventions
   - Define request parameters (path, query, body)
   - Specify response schema and status codes
   - Plan error responses and edge cases

3. Implement endpoint:
   - Create route/controller following project structure
   - Add input validation and sanitization
   - Implement business logic with proper separation
   - Add comprehensive error handling
   - Include appropriate logging
   - Implement rate limiting if needed

4. Security implementation:
   - Add authentication checks
   - Implement authorization/permission checks
   - Validate and sanitize all inputs
   - Prevent injection attacks
   - Add CORS configuration if needed
   - Implement request signing if required

5. Generate tests:
   - Unit tests for business logic
   - Integration tests for the endpoint
   - Test all response codes (200, 400, 401, 403, 404, 500)
   - Test edge cases and invalid inputs
   - Performance tests for heavy operations
   - Security tests (auth bypass attempts)

6. Create documentation:
   - OpenAPI/Swagger specification
   - Request/response examples
   - Error code documentation
   - Rate limiting information
   - Authentication requirements
   - Curl/HTTPie examples

7. Database/Service integration:
   - Create necessary database queries
   - Implement repository pattern if used
   - Add database migrations if needed
   - Configure connection pooling
   - Add caching layer if appropriate

Output:
- Complete endpoint implementation
- Comprehensive test suite
- API documentation
- Database migrations (if needed)
- Example client code