import azure.functions as func
import datetime
import json
import logging
import socket

app = func.FunctionApp()

@app.route(route="services", auth_level=func.AuthLevel.ANONYMOUS)
def services(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Obtém o corpo da solicitação HTTP como um objeto JSON
        req_body = req.get_json()

        # Obtém a chave IP e a chave de intervalo de porta do corpo da solicitação
        ip_key = req_body.get("ip")
        port_range_key = req_body.get("ports")
        port_result = ""
        socket.setdefaulttimeout(5)
        
        if "," in port_range_key:
            ports = port_range_key.split(",")
            for i in ports:
                logging.info(f"try port {i}")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if s.connect_ex((ip_key, int(i))) == 0:
                    logging.info(f"ABERTO {i}")
                    port_result += f"Porta ABERTA {i}\n"
                s.close()
            return func.HttpResponse(port_result, status_code=200)
        else:    
            for i in range(20, int(port_range_key)+1):
                logging.info(f"try port {i}")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if s.connect_ex((ip_key, i)) == 0:
                    logging.info("ABERTO")
                    port_result += f"Porta ABERTA {i}\n"
                s.close()
            return func.HttpResponse(port_result, status_code=200)
    except ValueError as e:
        # Se houver um erro ao tentar analisar o JSON, retorna uma resposta de erro
        return func.HttpResponse("Erro ao analisar JSON", status_code=400)
