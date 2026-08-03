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

echo "All prerequisites met! You are ready to deploy."
