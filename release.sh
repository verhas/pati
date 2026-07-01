#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if version argument provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Version argument required${NC}"
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 0.1.0"
    exit 1
fi

VERSION=$1

echo -e "${BLUE}Releasing pati v${VERSION}...${NC}"

# 1. Update version in __init__.py
echo "Updating version in src/pati/__init__.py..."
sed -i "" "s/__version__ = \".*\"/__version__ = \"${VERSION}\"/g" src/pati/__init__.py

# 2. Build
echo -e "${BLUE}Building package...${NC}"
./build.sh

# 3. Check PyPI credentials
echo -e "${BLUE}Checking PyPI credentials...${NC}"
if [ ! -f ~/.pypirc ]; then
    echo -e "${YELLOW}Warning: ~/.pypirc not found. You'll be prompted for credentials.${NC}"
fi

# 4. Upload to PyPI
echo -e "${BLUE}Uploading to PyPI...${NC}"
twine upload dist/* --verbose

# 5. Create git tag
echo -e "${BLUE}Creating git tag...${NC}"
git tag -a "v${VERSION}" -m "Release version ${VERSION}"
git push origin "v${VERSION}"

echo -e "${GREEN}✓ Release v${VERSION} complete!${NC}"
echo -e "${GREEN}✓ Package available at: https://pypi.org/project/patisserie/${VERSION}/${NC}"
