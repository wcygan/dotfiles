# Failure Detection And Gossip

Use this when studying heartbeats, suspicion, membership, dissemination, anti-entropy, or cluster liveness.

## Mental Model

Failure detection is a guess under uncertainty. A gossip protocol spreads observations through randomized peer exchange. The design goal is not perfect knowledge; it is useful convergence with bounded overhead and tolerable false positives.

## Key Invariants

- Suspicions carry time, incarnation, or version metadata.
- Membership updates eventually spread to reachable nodes.
- A suspected node can refute stale suspicion with newer evidence.

## Implementation Exercise

Build a SWIM-like membership simulator with ping, indirect ping, suspect, alive, and dead states.

## Tests And Failure Cases

Introduce packet loss and slow nodes. Track false positives, convergence time, and message count.

## Online References

- [SWIM: Scalable Weakly-consistent Infection-style Process Group Membership](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf)
- [The Phi Accrual Failure Detector](https://www.jaist.ac.jp/~defago/files/pdf/IS_RR_2004_010.pdf)
- [Lifeguard: SWIM-ing with Situational Awareness](https://arxiv.org/abs/1707.00788)

