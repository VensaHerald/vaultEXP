from open.globals import *
import vault_servs
import sys

# Access matter
va_matter = vault_servs.Vault_Service(SERVICE_FILE, SCOPES, STD_USER, STD_MATTER)
# Create service
va_matter.create_service()

input = sys.argv[1]

va_matter.create_exports(input)
