import http from 'node:http';
import { Readable } from 'node:stream';
import worker from './worker.mjs';

const port = Number(process.env.PORT || 4174);
const origin = 'http://127.0.0.1:' + port;
const env = {
  GROQ_API_KEY: process.env.GROQ_API_KEY,
  ASSETS: {
    fetch() { return new Response('Not found', { status: 404 }); }
  }
};

http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, origin);
    if (url.pathname === '/') {
      res.writeHead(302, { Location: '/pulse/' }).end();
      return;
    }
    const hasBody = !['GET', 'HEAD'].includes(req.method);
    const request = new Request(url, {
      method: req.method,
      headers: req.headers,
      ...(hasBody && { body: Readable.toWeb(req), duplex: 'half' })
    });
    const response = await worker.fetch(request, env);
    res.writeHead(response.status, Object.fromEntries(response.headers));
    res.end(Buffer.from(await response.arrayBuffer()));
  } catch {
    res.writeHead(400).end('Invalid request');
  }
}).listen(port, '127.0.0.1', () => console.log(origin + '/pulse/'));
