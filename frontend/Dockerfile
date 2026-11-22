FROM node:24-alpine

WORKDIR /blackbird

COPY package*.json ./

RUN npm clean-install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
