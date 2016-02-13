watchword
=========

Get notified when things don't happen.

Inspiration and Prior Art
-------------------------
I first learned about this concept (of alerting on non-events) from
[Dead Man's Snitch](https://deadmanssnitch.com/) and subsequently saw it on
[Cronitor](https://cronitor.io/). Open source implementations exist, such as
[Coal Mine](https://github.com/quantopian/coal-mine) and
[healthchecks](https://github.com/healthchecks/healthchecks) (which also comes
in a [hosted version](https://healthchecks.io/)).

Building my own implementation enables experimentation and provides learning
opportunities. Plus, it's fun!

I've greatly benefited from the architecture and design of healthchecks in
constructing watchword. Thank you, [cuu508](https://github.com/cuu508)!
