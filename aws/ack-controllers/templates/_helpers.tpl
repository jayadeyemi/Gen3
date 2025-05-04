The umbrella chart installs AWS ACK controllers selected in `values.yaml`.

• Each controller Deployment lives in the `ack-system` namespace (or the
  namespace you set in its block).
• Disable or tune a controller simply by editing values and running:
    helm upgrade --install <release> .

