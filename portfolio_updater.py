import os
import requests
import json

def update_portfolio_data():
    # Automatically detects your GitHub username from the repository path
    repo_full = os.environ.get("GITHUB_REPOSITORY", "parvathymanjusha-cpu/pulse-bot")
    username = repo_full.split("/")[0]
    
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
    print(f"Querying GitHub API for user: {username}")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch repository details: {response.status_code}")
        return
        
    repos = response.json()
    project_list = []
    
    for repo in repos:
        # Filter out forks to only include your original projects
        if not repo['fork']:
            project_data = {
                "name": repo["name"],
                "description": repo["description"] or "No description provided.",
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "language": repo["language"] or "Tech Stack Unassigned",
                "last_updated": repo["updated_at"]
            }
            project_list.append(project_data)
            
    # Output structured data to projects.json
    output_filename = "projects.json"
    with open(output_filename, "w") as f:
        json.dump(project_list, f, indent=4)
        
    print(f"Successfully compiled {len(project_list)} items into {output_filename}!")

if __name__ == "__main__":
    update_portfolio_data()