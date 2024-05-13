import streamlit as st
from urllib.parse import unquote

# Custom exception for handling specific client errors
class ClientException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

def extract_websocket_api_key():
    """Extract API key from WebSocket headers in Streamlit."""
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        if headers and 'Cookie' in headers:
            cookie_string = headers['Cookie']
            cookies = {k.strip(): unquote(v.strip()) for k, v in
                    (cookie.split('=') for cookie in cookie_string.split(';'))}
            if 'vps-auth-token' in cookies and len(cookies['vps-auth-token']) > 0:
                return cookies['vps-auth-token']
            else:
                raise ClientException(401, "vps-auth-token is not set in the WebSocket headers or it is empty")
        else:
            raise ClientException(400, "No cookies in WebSocket headers")
    except ImportError:
        raise ClientException(500, "Failed to import streamlit module")
    except Exception as e:
        raise ClientException(500, str(e))

def main():
    st.title('WebSocket API Key Checker')
    if st.button('Check vps-auth-token'):
        try:
            api_key = extract_websocket_api_key()
            st.success(f'vps-auth-token is set: {api_key}')
        except ClientException as e:
            st.error(f'Error ({e.status_code}): {e.message}')
        except Exception as e:
            st.error(f'Unexpected error: {str(e)}')

if __name__ == "__main__":
    main()

