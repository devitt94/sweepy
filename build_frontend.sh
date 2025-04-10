cd sweepstakes-ui/
npm run build
cd ..
mkdir -p sweepy/static
cp -r sweepstakes-ui/dist/* sweepy/static/
