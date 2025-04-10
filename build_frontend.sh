cd sweepy-ui/
npm run build
cd ..
mkdir -p sweepy/static
/bin/cp -r sweepy-ui/dist/* sweepy/static/
