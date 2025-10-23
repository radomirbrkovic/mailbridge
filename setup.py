from setuptools import setup, find_packages

setup(
    name="mailbridge",
    version="0.1.0",
    author="Radomir Brković",
    author_email="brkovic.radomir@gmail.com",
    description="Flexible mail delivery library supporting multiple providers (SMTP, SendGrid, Mailgun, SES, Postmark, Brevo)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/radomirbrkovic/mailbridge",
    packages=find_packages(),
    install_requires=[
        "requests",
        "boto3",
        "python-dotenv"
    ],
    python_requires=">=3.9",
)
