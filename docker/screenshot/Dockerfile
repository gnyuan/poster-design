FROM howard86/puppeteer_node:12 as DIST

ARG MYENV
WORKDIR /screenshot
COPY screenshot .
RUN npm install --no-progress --registry=http://192.168.0.79:4873/ \
    && echo "done"

CMD ["npm", "run", "dev"]
