# Workflow: MCP System, Hardware & Network Router

Load when: The user requests operations related to local file systems, docker, serial ports, IoT, network configuration, ssh, or cryptography.

## Available MCPs in this category:
- `filesystem`: Read/write/browse local files.
- `everything`: Fast file search on Windows.
- `docker`: Manage Docker containers.
- `serial` (mcp-serial): COM port, UART, Arduino communication.
- `mqtt`: IoT MQTT communication.
- `mcp-packet-tracer`: Cisco Packet Tracer control.
- `time`: Time and timezone logic.
- `virustotal`: Scan files for malware.
- `cryptography`: AES, RSA, SHA encryption/decryption.
- `sshmcp`: Remote SSH/SFTP control.
- `dns`: Domain name records and network diagnostics.

## Usage Guidelines:
1. Identify the target system/hardware element.
2. Select the corresponding MCP tool.
3. Check for necessary permissions (e.g., local admin rights for Docker or Serial).
4. For network tools (DNS, SSH, MQTT), ensure connectivity before execution.
