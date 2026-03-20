# ENFP8W7854SXSP

This repository packages two requested scaffolds:

- `genesis_block/` for a deterministic genesis package with a reproducible hash builder.
- `falconx_*` utilities for a defensive-only Falcon-X deployment, manifest, and IPO integration flow.

## Quick start

### Build the genesis block

```bash
cd genesis_block
python3 build_genesis.py
```

### Run the Falcon-X deployment

```bash
./falconx_full_deployment.sh
```

### Run the components individually

```bash
python3 falconx_toolset_orchestrator.py
python3 enhanced_ipo_defensive_integration.py
```
