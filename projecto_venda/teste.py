import smtplib

def test_smtp():
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('muquissicarlos@gmail.com', 'Mundo@1234')
        server.sendmail('muquissicarlos@gmail.com', 'teste@dominio.com', 'Este é um e-mail de teste.')
        server.quit()
        print("E-mail enviado com sucesso!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Erro de autenticação: {e}")
    except Exception as e:
        print(f"Erro: {e}")

test_smtp()
