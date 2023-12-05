# ZenoGuard GPT Review

ZenoGuard GPT Review is an automated code review tool that leverages the power of GPT-3 AI to review your pull requests and provide insightful comments. It's designed to help developers improve their code quality and catch potential issues early in the development process.

## Features

- Automated code reviews: ZenoGuard GPT Review automatically reviews your pull requests once they're opened, reopened, or synchronized.
- AI-powered insights: Leveraging the power of GPT-4, ZenoGuard provides detailed and insightful comments on your code.
- Easy to set up: With a simple GitHub Actions workflow, you can easily integrate ZenoGuard into your existing CI/CD pipeline.

## Setup

1. Add the ZenoGuard GPT Review GitHub Action to your repository's workflow. You can find the workflow file in `.github/workflows/auto-review.yml`.
2. Set up the necessary secrets in your repository settings:
   - `OPENAI_API_KEY`: Your OpenAI API key.

## Usage

Once set up, ZenoGuard GPT Review will automatically review new pull requests in your repository. It fetches the PR diff, sends it to the OpenAI API, and posts the AI-generated review as a comment on the PR.

## Contributing

Contributions are welcome! Please read the [LICENSE](LICENSE) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

ZenoGuard GPT Review is a tool to aid in code reviews and is not intended to replace human code reviews. Always review the AI-generated comments for accuracy.

## GitHub Marketplace

ZenoGuard GPT Review is available on the GitHub Marketplace. Visit [our page](https://github.com/marketplace/zenoguard-gpt-review) to install it on your repositories.

Happy coding!