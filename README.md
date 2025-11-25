**VISÃO GERAL** 🎯

**Chat Distribuído** `Versão 1.0`

- API REST para envio/listagem de mensagens, Apache Kafka como backbone de eventos, worker consumidor e MongoDB como Message Store.
- Fluxo: envio → Kafka → worker → atualização de status.

**Como rodar?**

- `git clone https://github.com/Aislla/chat_distribuido.git`
- `cd chat_distribuido`
- `docker compose up --build`
