FROM tooljet/tooljet-ce:latest

EXPOSE 80

CMD ["npm", "run", "start:prod"]
