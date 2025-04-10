cd sweepstakes-ui/
npm run build
cd ..
mkdir -p sweepy/static
/bin/cp -r sweepstakes-ui/dist/* sweepy/static/
