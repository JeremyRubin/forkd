# Fork Daemon


This python script detects versionbits based fork activations in Bitcoin Core
and then reorgs out blocks that would lead to an activation of a rule you don't
like.


Multiple soft forks in flight you don't like? No problem. Just run two forkd
instances.

# USE:

to reject taproot for a node with RPC port 1234 on 0.0.0.0 with user
imgonnadoit and password hunter2:

# DANGER THIS DOES REALLY WORK
```bash
./forkd.py 0.0.0.0 1234 imgonnadoit hunter2 taproot
```

# Requirements

Python 3, a running node, a desire to be on only the chain you like.

# FAQ

## I don't like generating RPC credentials, what can I do?
```bash
./forkd.py 0.0.0.0 1234 __cookie__ $(cat ~/.bitcoin/.cookie | cut -d ":" -f) taproot
```
_substitute ~/.bitcoin/.cookie with wherever your cookie file is_

## What if it crashes?

Maybe daemonize it so that the process gets restarted if it fails.

