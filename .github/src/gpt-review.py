import os
import requests


def get_pull_request_diff(repo_name, pr_id, github_token):
    """
    Fetch PR diff from GitHub API
    """
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_id}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code


def add_system_prompt(diff):
    """
    Add system prompt to the diff
    """
    system_promtpt = """
            Your name is Zeno, and you are the Senior AI Software Engineer at TextCortex. You specialize in crafting advanced AI assistants that aim to simplify tasks for people from all walks of life. As part of your commitment to excellence and continuous improvement, you are conducting a code review that will focus on scrutinizing this latest code patch.
                        
            **Review Criteria:**
            
            1. **Code Quality:** [[==========....................] x%] (add this at the beginning of section as a progress bar based on the result of the review)
               - **Clarity:** Is the intent of the code clear at first glance? (Also add ❌ or ✅ at the beginning of the bullet points to easily show if the review concludes it passed or failed mentioned topic.)
               - **Concision:** Is the code written as efficiently as possible?
               - **Consistency:** Does the code follow a consistent style and naming convention?
               - **Documentation:** Is the code well-documented, facilitating understanding and future maintenance?
            
            2. **Potential Bugs:** [[==========....................] x%] (add this at the beginning of section as a progress bar based on the result of the review)
               - **Error Handling:** Are potential errors adequately anticipated and handled?
               - **Edge Cases:** Has the code been tested against a variety of inputs, including edge cases?
               - **Performance:** Are there any parts of the code that could cause performance issues, such as unnecessary loops or resource-heavy operations?
               - **Security:** Does the code introduce any potential security vulnerabilities?
            
            Here is the code patch to review:\n\n
    """
    return system_promtpt + diff


def send_to_openai(prompt, openai_api_key):
    """
    Send prompt to OpenAI API and get the completion
    """
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": "gpt-4-1106-preview",
        "prompt": prompt,
        "temperature": 1,
        "max_tokens": 256,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def post_review_to_github(repo_name, pr_id, review_body, github_token):
    """
    Post review comment to GitHub PR
    """
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_id}/reviews"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": review_body,
        "event": "COMMENT"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()



def main():
    github_token = os.environ['GITHUB_TOKEN']
    openai_api_key = os.environ['OPENAI_API_KEY']
    repo_name = os.environ['GITHUB_REPOSITORY']
    pr_id = os.environ['PULL_REQUEST_ID']

    diff = get_pull_request_diff(repo_name, pr_id, github_token)
    diff_prompt = add_system_prompt(diff)
    review_completion = send_to_openai(diff_prompt, openai_api_key)
    post_review_to_github(repo_name, pr_id, review_completion, github_token)

if __name__ == '__main__':
    main()

