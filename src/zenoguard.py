import os
import requests


def get_pull_request_diff(repo_name, pr_id, github_token):
    """
    Fetch PR diff from GitHub API
    """
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_id}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3.diff",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code


def send_to_openai(prompt, key):
    """
    Send prompt to OpenAI API and get the completion
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}"}
    data = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {
                "role": "system",
                "content": "Your name is Zeno, and you are the Senior AI Software Engineer at TextCortex."
                " You specialize in crafting advanced AI assistants that aim to simplify tasks for people "
                "from all walks of life. As part of your commitment to excellence and continuous improvement,"
                " you are conducting a code review that will focus on scrutinizing this latest code patch.\n\n"
                "**Review Criteria:**\n\n1. **Code Quality:**\n- **Clarity:** Is the intent of the code clear at first"
                " glance? (Also add ❌ or ✅ at the beginning of the bullet points to easily show if the "
                "review concludes it passed or failed mentioned topic.)\n- **Concision:** Is the code "
                "written as efficiently as possible?\n- **Consistency:** Does the code follow a consistent "
                "style and naming convention?\n- **Documentation:** Is the code well-documented, "
                "facilitating understanding and future maintenance?\n\n2. **Potential Bugs:**\n- **Error "
                "Handling:** Are potential errors adequately anticipated and handled?\n- **Edge Cases:** "
                "Has the code been tested against a variety of inputs, including edge cases?\n- "
                "**Performance:** Are there any parts of the code that could cause performance issues, "
                "such as unnecessary loops or resource-heavy operations?\n- **Security:** Does the code "
                "introduce any potential security vulnerabilities?",
            },
            {
                "role": "user",
                "content": f"Here is the code diff/patch to review:\n\n{prompt}",
            },
        ],
        "temperature": 1,
        "max_tokens": 4096,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("choices")[0].get("message").get("content")
    else:
        response.raise_for_status()


def post_review_to_github(repo_name, pr_id, review_body, github_token):
    """
    Post review comment to GitHub PR
    """
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_id}/reviews"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"body": review_body, "event": "COMMENT"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()


def main():
    github_token = os.environ["GITHUB_TOKEN"]
    openai_api_key = os.environ["OPENAI_API_KEY"]
    repo_name = os.environ["GITHUB_REPOSITORY"]
    pr_id = os.environ["PULL_REQUEST_ID"]

    diff = get_pull_request_diff(repo_name, pr_id, github_token)
    review_completion = send_to_openai(diff, openai_api_key)
    post_review_to_github(repo_name, pr_id, review_completion, github_token)


if __name__ == "__main__":
    main()
