#!/bin/bash
echo "Checking prerequisites..."

if ! command -v git &> /dev/null
then
    echo "❌ Git could not be found. Please install Git."
    exit 1
else
    echo "✅ Git is installed."
fi

if ! command -v terraform &> /dev/null
then
    echo "❌ Terraform could not be found. Please install Terraform."
    exit 1
else
    echo "✅ Terraform is installed."
fi

if ! command -v ruby &> /dev/null
then
    echo "❌ Ruby could not be found. Please install Ruby."
    exit 1
else
    echo "✅ Ruby is installed."
fi

if ! command -v bundle &> /dev/null
then
    echo "❌ Bundler could not be found. Please install Bundler (run: gem install bundler)."
    exit 1
else
    echo "✅ Bundler is installed."
fi

echo "Setting up local Ruby environment..."
bundle config set path 'vendor/bundle'
bundle install

echo "All prerequisites met and local dependencies installed!"
echo "To run the Jekyll website locally, execute:"
echo "  bundle exec jekyll serve --baseurl \"\""
