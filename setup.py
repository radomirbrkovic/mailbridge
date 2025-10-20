from setuptools import setup, find_packages

setup(
    name="mailbridge",
    version="0.1.0",
    description="Unified email sending interface for multiple providers (SMTP, SendGrid, SES...)",
    author="Radomir Brkovic",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.8",
)