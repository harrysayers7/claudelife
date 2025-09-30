---
date: 2025-09-29 20:31
relation:
  - "[[mcp]]"
  - "[[Instructions]]"
tags:
  - todo
description: Also includes FASTMCP Cloud
---
https://gofastmcp.com/deployment/self-hosted?hl=en-AU

# Self-Hosted Remote MCP

> Deploy your FastMCP server as a remote MCP service accessible via URL

<Tip>
  STDIO transport is perfect for local development and desktop applications. But to unlock the full potential of MCP—centralized services, multi-client access, and network availability—you need remote HTTP deployment.
</Tip>

This guide walks you through deploying your FastMCP server as a remote MCP service that's accessible via a URL. Once deployed, your MCP server will be available over the network, allowing multiple clients to connect simultaneously and enabling integration with cloud-based LLM applications. This guide focuses specifically on remote MCP deployment, not local STDIO servers.

## Choosing Your Approach

FastMCP provides two ways to deploy your server as an HTTP service. Understanding the trade-offs helps you choose the right approach for your needs.

The **direct HTTP server** approach is simpler and perfect for getting started quickly. You modify your server's `run()` method to use HTTP transport, and FastMCP handles all the web server configuration. This approach works well for standalone deployments where you want your MCP server to be the only service running on a port.

The **ASGI application** approach gives you more control and flexibility. Instead of running the server directly, you create an ASGI application that can be served by production-grade servers like Uvicorn or Gunicorn. This approach is better when you need advanced server features like multiple workers, custom middleware, or when you're integrating with existing web applications.

### Direct HTTP Server

The simplest way to get your MCP server online is to use the built-in `run()` method with HTTP transport. This approach handles all the server configuration for you and is ideal when you want a standalone MCP server without additional complexity.

```python server.py
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def process_data(input: str) -> str:
    """Process data on the server"""
    return f"Processed: {input}"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

Run your server with a simple Python command:

```bash
python server.py
```

Your server is now accessible at `http://localhost:8000/mcp/` (or use your server's actual IP address for remote access).

This approach is ideal when you want to get online quickly with minimal configuration. It's perfect for internal tools, development environments, or simple deployments where you don't need advanced server features. The built-in server handles all the HTTP details, letting you focus on your MCP implementation.

### ASGI Application

For production deployments, you'll often want more control over how your server runs. FastMCP can create a standard ASGI application that works with any ASGI server like Uvicorn, Gunicorn, or Hypercorn. This approach is particularly useful when you need to configure advanced server options, run multiple workers, or integrate with existing infrastructure.

```python app.py
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def process_data(input: str) -> str:
    """Process data on the server"""
    return f"Processed: {input}"

# Create ASGI application
app = mcp.http_app()
```

Run with any ASGI server - here's an example with Uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Your server is accessible at the same URL: `http://localhost:8000/mcp/` (or use your server's actual IP address for remote access).

The ASGI approach shines in production environments where you need reliability and performance. You can run multiple worker processes to handle concurrent requests, add custom middleware for logging or monitoring, integrate with existing deployment pipelines, or mount your MCP server as part of a larger application. This flexibility makes it the preferred choice for serious deployments.

## Configuring Your Server

### Custom Path

By default, your MCP server is accessible at `/mcp/` on your domain. You can customize this path to fit your URL structure or avoid conflicts with existing endpoints. This is particularly useful when integrating MCP into an existing application or following specific API conventions.

```python
# Option 1: With mcp.run()
mcp.run(transport="http", host="0.0.0.0", port=8000, path="/api/mcp/")

# Option 2: With ASGI app
app = mcp.http_app(path="/api/mcp/")
```

Now your server is accessible at `http://localhost:8000/api/mcp/`.

### Authentication

<Warning>
  Authentication is **highly recommended** for remote MCP servers. Some LLM clients require authentication for remote servers and will refuse to connect without it.
</Warning>

FastMCP supports multiple authentication methods to secure your remote server. See the [Authentication Overview](/servers/auth/authentication) for complete configuration options including Bearer tokens, JWT, and OAuth.

### Health Checks

Health check endpoints are essential for monitoring your deployed server and ensuring it's responding correctly. FastMCP allows you to add custom routes alongside your MCP endpoints, making it easy to implement health checks that work with both deployment approaches.

```python
from starlette.responses import JSONResponse

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})
```

This health endpoint will be available at `http://localhost:8000/health` and can be used by load balancers, monitoring systems, or deployment platforms to verify your server is running.

## Integration with Web Frameworks

If you already have a web application running, you can add MCP capabilities by mounting a FastMCP server as a sub-application. This allows you to expose MCP tools alongside your existing API endpoints, sharing the same domain and infrastructure. The MCP server becomes just another route in your application, making it easy to manage and deploy.

For detailed integration guides, see:

* [FastAPI Integration](/integrations/fastapi)
* [ASGI / Starlette Integration](/integrations/asgi)

Here's a quick example showing how to add MCP to an existing FastAPI application:

```python
from fastapi import FastAPI
from fastmcp import FastMCP

# Your existing API
api = FastAPI()

@api.get("/api/status")
def status():
    return {"status": "ok"}

# Create your MCP server
mcp = FastMCP("API Tools")

@mcp.tool
def query_database(query: str) -> dict:
    """Run a database query"""
    return {"result": "data"}

# Mount MCP at /mcp
api.mount("/mcp", mcp.http_app())

# Run with: uvicorn app:api --host 0.0.0.0 --port 8000
```

Your existing API remains at `http://localhost:8000/api/` while MCP is available at `http://localhost:8000/mcp/`.

## Production Deployment

### Running with Uvicorn

When deploying to production, you'll want to optimize your server for performance and reliability. Uvicorn provides several options to improve your server's capabilities, including running multiple worker processes to handle concurrent requests and enabling enhanced logging for monitoring.

```bash
# Install uvicorn with standard extras for better performance
pip install 'uvicorn[standard]'

# Run with multiple workers for better concurrency
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# Enable detailed logging for monitoring
uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

### Environment Variables

Production deployments should never hardcode sensitive information like API keys or authentication tokens. Instead, use environment variables to configure your server at runtime. This keeps your code secure and makes it easy to deploy the same code to different environments with different configurations.

Here's an example using bearer token authentication (though OAuth is recommended for production):

```python
import os
from fastmcp import FastMCP
from fastmcp.server.auth import BearerTokenAuth

# Read configuration from environment
auth_token = os.environ.get("MCP_AUTH_TOKEN")
if auth_token:
    auth = BearerTokenAuth(token=auth_token)
    mcp = FastMCP("Production Server", auth=auth)
else:
    mcp = FastMCP("Production Server")

app = mcp.http_app()
```

Deploy with your secrets safely stored in environment variables:

```bash
MCP_AUTH_TOKEN=secret uvicorn app:app --host 0.0.0.0 --port 8000
```

## Testing Your Deployment

Once your server is deployed, you'll need to verify it's accessible and functioning correctly. For comprehensive testing strategies including connectivity tests, client testing, and authentication testing, see the [Testing Your Server](/development/tests) guide.

## Hosting Your Server

This guide has shown you how to create an HTTP-accessible MCP server, but you'll still need a hosting provider to make it available on the internet. Your FastMCP server can run anywhere that supports Python web applications:

* **Cloud VMs** (AWS EC2, Google Compute Engine, Azure VMs)
* **Container platforms** (Cloud Run, Container Instances, ECS)
* **Platform-as-a-Service** (Railway, Render, Vercel)
* **Edge platforms** (Cloudflare Workers)
* **Kubernetes clusters** (self-managed or managed)

The key requirements are Python 3.10+ support and the ability to expose an HTTP port. Most providers will require you to package your server (requirements.txt, Dockerfile, etc.) according to their deployment format. For managed, zero-configuration deployment, see [FastMCP Cloud](/deployment/fastmcp-cloud).

# FastMCP Cloud

> The fastest way to deploy your MCP server

[FastMCP Cloud](https://fastmcp.cloud) is a managed platform for hosting MCP servers, built by the FastMCP team. While the FastMCP framework will always be fully open-source, we created FastMCP Cloud to solve the deployment challenges we've seen developers face. Our goal is to provide the absolute fastest way to make your MCP server available to LLM clients like Claude and Cursor.

FastMCP Cloud is a young product and we welcome your feedback. Please join our [Discord](https://discord.com/invite/aGsSC3yDF4) to share your thoughts and ideas, and you can expect to see new features and improvements every week.

<Note>
  FastMCP Cloud supports both **FastMCP 2.0** servers and also **FastMCP 1.0** servers that were created with the official MCP Python SDK.
</Note>

<Tip>
  FastMCP Cloud is completely free while in beta!
</Tip>

## Prerequisites

To use FastMCP Cloud, you'll need a [GitHub](https://github.com) account. In addition, you'll need a GitHub repo that contains a FastMCP server instance. If you don't want to create one yet, you can proceed to [step 1](#step-1-create-a-project) and use the FastMCP Cloud quickstart repo.

Your repo can be public or private, but must include at least a Python file that contains a FastMCP server instance.

<Tip>
  To ensure your file is compatible with FastMCP Cloud, you can run `fastmcp inspect <file.py:server_object>` to see what FastMCP Cloud will see when it runs your server.
</Tip>

If you have a `requirements.txt` or `pyproject.toml` in the repo, FastMCP Cloud will automatically detect your server's dependencies and install them for you. Note that your file *can* have an `if __name__ == "__main__"` block, but it will be ignored by FastMCP Cloud.

For example, a minimal server file might look like:

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

## Getting Started

There are just three steps to deploying a server to FastMCP Cloud:

### Step 1: Create a Project

Visit [fastmcp.cloud](https://fastmcp.cloud) and sign in with your GitHub account. Then, create a project. Each project corresponds to a GitHub repo, and you can create one from either your own repo or using the FastMCP Cloud quickstart repo.

<img src="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/quickstart.png?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=a98be26fc2265a8b74476d1747287e53" alt="FastMCP Cloud Quickstart Screen" data-og-width="2656" width="2656" data-og-height="1808" height="1808" data-path="assets/images/fastmcp_cloud/quickstart.png" data-optimize="true" data-opv="2" srcset="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/quickstart.png?w=280&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=6574699628440718a296eecb1c9c1d34 280w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/quickstart.png?w=560&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=740b6cb6a21b2bd165f0348b7f70f1bb 560w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/quickstart.png?w=840&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=183e219af3c0d9bcc87a7e192f9d861a 840w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/quickstart.png?w=1100&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=5b22225c6d1f2fd48e461f6e7c8a4137 1100w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/quickstart.png?w=1650&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=9de436ae99e8e175268ab0415ae69373 1650w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/quickstart.png?w=2500&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=b2320ef39fff5ff3a00d5c09787fefc8 2500w" />

Next, you'll be prompted to configure your project.

<img src="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/create_project.png?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=4c221cd0734a6fd7b634970ac0aff73a" alt="FastMCP Cloud Configuration Screen" data-og-width="2656" width="2656" data-og-height="1808" height="1808" data-path="assets/images/fastmcp_cloud/create_project.png" data-optimize="true" data-opv="2" srcset="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/create_project.png?w=280&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=168c690ac8a8e5098b05c8e23cf9173b 280w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/create_project.png?w=560&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=16cd0ee3977040439e9982e8aa438ffe 560w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/create_project.png?w=840&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=4b0265a257b6a9510c85863da1b5e17a 840w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/create_project.png?w=1100&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=e898cfe81f01bf14312d98902be41b5c 1100w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/create_project.png?w=1650&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=d97a7ddad8e60c86e303faa8e37d784c 1650w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/create_project.png?w=2500&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=51b9fa2763dc5064c1eef4f8f90af77a 2500w" />

The configuration screen lets you specify:

* **Name**: The name of your project. This will be used to generate a unique URL for your server.
* **Entrypoint**: The Python file containing your FastMCP server (e.g., `echo.py`). This field has the same syntax as the `fastmcp run` command, for example `echo.py:my_server` to specify a specific object in the file.
* **Authentication**: If disabled, your server is open to the public. If enabled, only other members of your FastMCP Cloud organization will be able to connect.

Note that FastMCP Cloud will automatically detect yours server's Python dependencies from either a `requirements.txt` or `pyproject.toml` file.

### Step 2: Deploy Your Server

Once you configure your project, FastMCP Cloud will:

1. Clone the repository
2. Build your FastMCP server
3. Deploy it to a unique URL
4. Make it immediately available for connections

<img src="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/deployment.png?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=cdb7389c54a0d9d7853807b4bf996d63" alt="FastMCP Cloud Deployment Screen" data-og-width="2656" width="2656" data-og-height="1808" height="1808" data-path="assets/images/fastmcp_cloud/deployment.png" data-optimize="true" data-opv="2" srcset="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/deployment.png?w=280&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=a218792290c0798cd9e79f479904d245 280w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/deployment.png?w=560&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=a06622288cdbf1c267175e36965c4fb1 560w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/deployment.png?w=840&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=69c5e285cb70f1192f96caafa79eb26e 840w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/deployment.png?w=1100&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=831d6f9609c2a70d59ae087f4064b140 1100w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/deployment.png?w=1650&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=3247286a4749d1cfbe408ac6c3e02fce 1650w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/deployment.png?w=2500&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=f6b3a204d808cad20b40f200e2e40d7a 2500w" />

FastMCP Cloud will monitor your repo and redeploy your server whenever you push a change to the `main` branch. In addition, FastMCP Cloud will build and deploy servers for every PR your open, hosting them on unique URLs, so you can test changes before updating your production server.

### Step 3: Connect to Your Server

Once your server is deployed, it will be accessible at a URL like:

```
https://your-project-name.fastmcp.app/mcp
```

You should be able to connect to it as soon as you see the deployment succeed! FastMCP Cloud provides instant connection options for popular LLM clients:

<img src="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/connect.png?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=ec716be49f8e43028eb872ff3ac95624" alt="FastMCP Cloud Connection Screen" data-og-width="2568" width="2568" data-og-height="1720" height="1720" data-path="assets/images/fastmcp_cloud/connect.png" data-optimize="true" data-opv="2" srcset="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/connect.png?w=280&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=10053e00e12a0d29376fa9e36f6db5e4 280w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/connect.png?w=560&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=d8ea20e041da1d97f4cc681a36d7a09b 560w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/connect.png?w=840&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=8da73612790ad0cbd5e97958ba590ee5 840w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/connect.png?w=1100&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=6db33a68f39c1796ce24fff8781a9add 1100w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/connect.png?w=1650&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=beb88faa10fd0c9dba4ef5ec2b8ce955 1650w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/assets/images/fastmcp_cloud/connect.png?w=2500&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=fb9b2640011b3757a9a0cdcb4b4449c4 2500w" />
