# Build frontend

cd sweepy-ui/
npm run build-dev
cd ..
rm -rf sweepy/static
mkdir -p sweepy/static
/bin/cp -r sweepy-ui/dist/* sweepy/static/

poetry run uvicorn sweepy.api:app --reload