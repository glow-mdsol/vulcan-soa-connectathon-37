# Quick Start Guide

## First Time Setup

### 1. Create .env file
Copy the example configuration:
```bash
cp example.env .env
```

### 2. Edit .env file
Open `.env` in your editor and set the values:
```env
ENDPOINT_URL=https://your-fhir-server.com/fhir
FHIR_USERNAME=your-username
FHIR_PASSWORD=your-password
```

### 3. Test Configuration
```bash
poetry run python test_config.py
```

You should see:
```
✓ Config loaded successfully!
  Endpoint: https://your-fhir-server.com/fhir
  Username: your-username
  Password: ************
```

### 4. Launch the UI
```bash
./run_ui.sh
```

Or:
```bash
poetry run streamlit run src/tasks/ui.py
```

The UI will open at: http://localhost:8501

## Troubleshooting

### "Configuration Error" in UI
- Make sure `.env` file exists in the project root
- Check that all required variables are set:
  - `ENDPOINT_URL`
  - `FHIR_USERNAME`
  - `FHIR_PASSWORD`
- Run `poetry run python test_config.py` to verify

### "No research subjects found"
- Verify your FHIR server is accessible
- Check credentials are correct
- Make sure the server has ResearchSubject resources

### Port already in use
Run on a different port:
```bash
poetry run streamlit run src/tasks/ui.py --server.port 8502
```

## Environment Variables

### Required
- `ENDPOINT_URL` - FHIR server endpoint URL
- `FHIR_USERNAME` - Authentication username
- `FHIR_PASSWORD` - Authentication password

### Optional
- `CLIENT_ID` - OAuth client ID (if using OAuth)
- `PRIVATE_KEY_PATH` - Path to private key file
- `TOKEN_URL` - OAuth token endpoint

## File Locations

- Configuration: `.env` (root directory)
- Example config: `example.env`
- Test script: `test_config.py`
- UI launcher: `run_ui.sh`
- UI code: `src/tasks/ui.py`
