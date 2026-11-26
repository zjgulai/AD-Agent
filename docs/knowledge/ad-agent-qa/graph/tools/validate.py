#!/usr/bin/env python3
"""Validate ad-ops graph instance shards against schema.

Checks: JSON parse, node @type in classes.json, edge @type in relations.json,
edge endpoints resolve to nodes, every edge carries ref (provenance),
relation domain/range respected (best-effort, wildcard-aware).

Usage: python3 validate.py [instances_dir]
Exit 0 = all shards pass; prints per-shard stats.
"""
import json, sys, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
KB = os.path.abspath(os.path.join(ROOT, "..", ".."))
SCHEMA = os.path.join(KB, "graph", "schema")

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def main():
    inst_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(KB, "graph", "instances")
    classes = {c["id"]: c for c in load(os.path.join(SCHEMA, "classes.json"))["classes"]}
    rels = {r["id"]: r for r in load(os.path.join(SCHEMA, "relations.json"))["relations"]}
    errors, warnings = [], []

    for nf in sorted(glob.glob(os.path.join(inst_dir, "*.nodes.json"))):
        shard = os.path.basename(nf).replace(".nodes.json", "")
        ef = os.path.join(inst_dir, shard + ".edges.json")
        nodes_doc, edges_doc = load(nf), load(ef)
        nodes = {n["@id"]: n for n in nodes_doc["nodes"]}
        edges = edges_doc["edges"]
        defaults = nodes_doc.get("defaults", {}) | edges_doc.get("defaults", {})

        # node checks
        for n in nodes_doc["nodes"]:
            t = n.get("@type")
            if t not in classes:
                errors.append(f"{shard}: node {n['@id']} unknown @type {t}")
            if not n.get("src"):
                warnings.append(f"{shard}: node {n['@id']} missing src provenance")

        # edge checks
        for i, e in enumerate(edges):
            eid = f"{shard}:edge[{i}] {e.get('@type')} {e.get('source')}->{e.get('target')}"
            rt = e.get("@type")
            if rt not in rels:
                errors.append(f"{eid}: unknown relation {rt}")
                continue
            if not e.get("ref"):
                errors.append(f"{eid}: missing ref provenance")
            for k in ("source", "target"):
                if e.get(k) not in nodes:
                    errors.append(f"{eid}: {k} {e.get(k)} not in nodes")
            # lifecycle fields (defaults count as satisfied)
            for f in ("status", "confidence", "freshness", "last_verified"):
                if f not in e and f not in defaults:
                    warnings.append(f"{eid}: missing lifecycle field {f}")
            # domain/range (skip if endpoints unknown)
            spec = rels[rt]
            s_t = nodes.get(e.get("source"), {}).get("@type")
            t_t = nodes.get(e.get("target"), {}).get("@type")
            if s_t and t_t:
                def ok(spec_list, t):
                    return any(x == t or x == "ad:*" or (x.endswith(":*") and t.startswith(x[:-1])) for x in spec_list)
                if not ok(spec.get("domain", ["ad:*"]), s_t):
                    errors.append(f"{eid}: source type {s_t} outside domain {spec.get('domain')}")
                if not ok(spec.get("range", ["ad:*"]), t_t):
                    errors.append(f"{eid}: target type {t_t} outside range {spec.get('range')}")

        print(f"{shard}: {len(nodes)} nodes, {len(edges)} edges")
        # quick stats by relation
        from collections import Counter
        c = Counter(e["@type"] for e in edges)
        print("   " + ", ".join(f"{k.replace('ad:','')}:{v}" for k, v in c.most_common()))

    for w in warnings[:30]:
        print("WARN:", w)
    if len(warnings) > 30:
        print(f"... +{len(warnings)-30} more warnings")
    for e in errors:
        print("ERROR:", e)
    print(f"\n{'FAIL' if errors else 'PASS'}: {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
