# tech-spec.md
## v1 Technical Specification for idea-spark

### Stack

* **Language**: Node.js (14.x)
* **Framework**: Express.js (4.x)
* **Runtime**: Docker (20.x)
* **Database**: MongoDB (4.x) with Mongoose (5.x) ORM
* **Cache**: Redis (6.x) for session storage and API rate limiting
* **Message Queue**: RabbitMQ (3.x) for asynchronous task processing

### Hosting

* **Primary Platform**: AWS (Free Tier eligible)
* **Secondary Platform**: DigitalOcean (1-click droplet with 512MB RAM and 1 CPU)
* **Containerization**: Docker Hub for image storage and deployment

### Data Model

* **Collections**:
	+ `ideas`: stores generated product ideas
		- `id` (string): unique identifier
		- `title` (string): idea title
		- `description` (string): idea description
		- `tags` (array): relevant tags
	+ `users`: stores user information
		- `id` (string): unique identifier
		- `email` (string): user email
		- `password` (string): hashed user password
	+ `sessions`: stores user session data
		- `id` (string): unique identifier
		- `userId` (string): associated user ID
		- `expires` (date): session expiration date
* **Tables**:
	+ `idea_sparks`: stores generated idea sparks
		- `id` (string): unique identifier
		- `ideaId` (string): associated idea ID
		- `spark` (string): generated spark

### API Surface

* **Endpoints**:
	1. `GET /ideas`: retrieve a list of generated product ideas
	2. `POST /ideas`: create a new product idea
		- Request Body: `title` (string), `description` (string), `tags` (array)
	3. `GET /ideas/{id}`: retrieve a specific product idea by ID
	4. `PUT /ideas/{id}`: update a specific product idea
		- Request Body: `title` (string), `description` (string), `tags` (array)
	5. `DELETE /ideas/{id}`: delete a specific product idea
	6. `POST /users`: create a new user account
		- Request Body: `email` (string), `password` (string)
	7. `POST /sessions`: create a new user session
		- Request Body: `email` (string), `password` (string)
	8. `GET /sessions/{id}`: retrieve a specific user session by ID
	9. `DELETE /sessions/{id}`: delete a specific user session
	10. `GET /idea_sparks`: retrieve a list of generated idea sparks
	11. `POST /idea_sparks`: create a new idea spark
		- Request Body: `ideaId` (string), `spark` (string)

### Security Model

* **Authentication**: JSON Web Tokens (JWT) for user authentication
* **Authorization**: Role-Based Access Control (RBAC) for user permissions
* **Secrets**: Environment variables for storing sensitive data (e.g., API keys, database credentials)
* **IAM**: AWS IAM for managing user access and permissions

### Observability

* **Logs**: Winston (3.x) for logging and error tracking
* **Metrics**: Prometheus (2.x) for monitoring and performance metrics
* **Traces**: OpenTelemetry (0.x) for distributed tracing and debugging

### Build/CI

* **Build Tool**: npm (6.x) for package management and build automation
* **CI Tool**: GitHub Actions (2.x) for continuous integration and deployment
* **Containerization**: Docker (20.x) for image creation and deployment
* **Testing Framework**: Jest (26.x) for unit testing and integration testing