GitLab MCP Server
A comprehensive Model Context Protocol (MCP) server that provides 72+ tools for complete GitLab integration with AI assistants like Claude.

Quick Start
1. Get a GitLab Token:

Go to GitLab → Profile Settings → Access Tokens
Create token with api and read_user scopes
Copy the generated token
2. Use with Claude Code:

claude mcp add gitlab --env GITLAB_TOKEN=your-gitlab-token --scope user -- npx @sekora/gitlab-mcp
3. Add to Claude Desktop config:

{
  "mcpServers": {
    "gitlab": {
      "command": "npx",
      "args": ["@sekora/gitlab-mcp"],
      "env": {
        "GITLAB_TOKEN": "your-gitlab-token"
      }
    }
  }
}
Features
72+ GitLab Tools: Complete coverage of GitLab's API for pipelines, jobs, issues, merge requests, and more
Natural Language Interface: Use the ask prompt to interact with GitLab using conversational commands
Smart Analysis: Specialized prompts for code review, pipeline analysis, and Terragrunt plan review
Real-time Monitoring: Pipeline and job monitoring with intelligent alerts and status tracking
Security Scanning: SAST, dependency, container, and license scanning integration
Multi-Instance Support: Connect to multiple GitLab instances (gitlab.com, self-hosted, etc.)
Prompts
/ask - Natural language interface for GitLab operations
/code-review - AI-powered code review analysis
/commit - Intelligent commit workflow with pipeline monitoring
/job-analyzer - Deep analysis of CI/CD job failures
/pipeline-analyzer - Comprehensive pipeline performance analysis
/pipeline-timing - Detailed timing analysis for optimization
Tools
Issue Management
gitlab_issue_create - Create new issues with metadata
gitlab_issue_list - List and search issues
gitlab_issue_details - Get detailed issue information
gitlab_issue_update - Update issue properties
gitlab_issue_close - Close issues with resolution notes
gitlab_issue_link - Link issues to other issues/MRs
Pipeline Management
gitlab_pipeline_status - Get pipeline status
gitlab_pipeline_list - List pipelines with filtering
gitlab_pipeline_details - Detailed pipeline information
gitlab_pipeline_jobs - List jobs in a pipeline
gitlab_pipeline_logs - Get pipeline execution logs
gitlab_pipeline_retry - Retry failed pipelines
gitlab_pipeline_cancel - Cancel running pipelines
gitlab_pipeline_trigger - Trigger new pipelines
gitlab_pipeline_metrics - Pipeline performance analytics
gitlab_pipeline_dashboard - Comprehensive status dashboard
Job Management
gitlab_job_status - Get job status and details
gitlab_job_list - List jobs with filtering
gitlab_job_logs - Get job execution logs
gitlab_job_trace - Real-time job trace
gitlab_job_retry - Retry failed jobs
gitlab_job_cancel - Cancel running jobs
gitlab_job_play - Trigger manual jobs
gitlab_job_artifacts - List and download artifacts
Merge Request Management
gitlab_mr_create - Create new merge requests
gitlab_mr_list - List and search merge requests
gitlab_mr_details - Get detailed MR information
gitlab_mr_approve - Approve merge requests
gitlab_mr_merge - Merge approved requests
gitlab_mr_get_comments - Manage review comments
gitlab_mr_conflicts - Check merge conflicts
Repository Management
gitlab_branch_list - List repository branches
gitlab_branch_create - Create new branches
gitlab_branch_compare - Compare branches/commits
gitlab_file_read - Read file contents
gitlab_file_update - Update file contents
gitlab_commit_history - Get commit history
gitlab_tag_create - Create repository tags
gitlab_release_manage - Manage releases
Security & Quality
gitlab_security_scan - Comprehensive security scanning
gitlab_sast_results - Static analysis security testing
gitlab_dependency_scan - Dependency vulnerability scanning
gitlab_container_scan - Container image security scanning
gitlab_license_scan - License compliance scanning
gitlab_code_quality - Code quality metrics
Project Administration
gitlab_project_settings - View and update project settings
gitlab_project_members - Manage project members
gitlab_project_analytics - Project analytics and insights
gitlab_access_tokens - Manage project access tokens
gitlab_deploy_keys - Manage SSH deploy keys
gitlab_project_hooks - Manage project webhooks
Readme
Keywords
none
Package Sidebar
Install
npm i @sekora/gitlab-mcp