#!/usr/bin/env python3
import os
import argparse
from datetime import datetime

SHOTGRID_ROOT = "/dd/shotgrid"
GLOBAL_TOOLS_ROOT = "/dd/tools/rocky9_64"

# --------------------------------------------------
# Shortcuts
# --------------------------------------------------

RC_RELATIVE = os.path.join("tools", "rocky9_64", "extension", "dd", "contexts")
RC_GLOBAL = "/dd/tools/rocky9_64/extension/dd/contexts"

SHORTCUTS = {
    # special dual-scope shortcut
    "rc": RC_RELATIVE,

    # show-relative shortcuts
    "dd7": '/dd/tools/cent7_64/package',
    "dd9": '/dd/tools/rocky9_64/package',

    # global-only shortcuts
    "ddb": "/dd/tools/rocky9_64/bin",
    "ng": "/dd/tools/rocky9_64/package/nuke_gizmos/0.26.2_ayon",
    "imt": "/dd/tools/rocky9_64/package/indiamayatools/maya2022_ayon",
    "i3t": "/dd/tools/rocky9_64/package/india3detools/5.5.0_ayon",
}

# --------------------------------------------------

def today():
    return datetime.now().strftime("%Y%m%d")


def main():
    parser = argparse.ArgumentParser(
        description="flash – fast cd helper for ShotGrid / tools paths"
    )
    parser.add_argument("-s", "--show", help="Show name (e.g. RND)")
    parser.add_argument("-i", "--incoming", nargs="?", const="TODAY")
    parser.add_argument("-o", "--outgoing", nargs="?", const="TODAY")
    parser.add_argument("tokens", nargs="*")

    args = parser.parse_args()

    # --------------------------------------------------
    # 1) SHORTCUT MODE
    # --------------------------------------------------
    if args.tokens and args.tokens[0] in SHORTCUTS:
        key = args.tokens[0]
        shortcut = SHORTCUTS[key]

        # rc → dual behavior
        if key == "rc":
            if args.show:
                print(os.path.join(SHOTGRID_ROOT, args.show, shortcut))
            else:
                print(RC_GLOBAL)
            return
        # absolute shortcuts (ddb, ng, imt, etc.)
        if os.path.isabs(shortcut):
            print(shortcut)
            return

        # show-relative shortcuts (dd7, dd9)
        if not args.show:
            parser.error(f"shortcut '{key}' requires -s SHOW")

        print(os.path.join(SHOTGRID_ROOT, args.show, shortcut))
        return

    # --------------------------------------------------
    # 2) Everything else REQUIRES -s
    # --------------------------------------------------
    if not args.show:
        parser.error("the following arguments are required: -s/--show")

    show_root = os.path.join(SHOTGRID_ROOT, args.show)

    # --------------------------------------------------
    # 3) Incoming / Outgoing
    # --------------------------------------------------
    if args.incoming is not None:
        date = today() if args.incoming == "TODAY" else args.incoming
        print(os.path.join(show_root, "REF", "CLIENT_VAULT", "incoming", date))
        return

    if args.outgoing is not None:
        date = today() if args.outgoing == "TODAY" else args.outgoing
        print(os.path.join(show_root, "REF", "CLIENT_VAULT", "outgoing", date))
        return

    # --------------------------------------------------
    # 4) etc / setc shortcuts
    # --------------------------------------------------
    if args.tokens:
        if args.tokens[0] == "etc":
            print(os.path.join(show_root, "etc"))
            return
        if args.tokens[0] == "setc":
            print(os.path.join(show_root, "SHARED", "etc"))
            return

    # --------------------------------------------------
    # 5) Default navigation: dept / shot / user
    # --------------------------------------------------
    path = show_root

    if args.tokens:
        path = os.path.join(path, args.tokens[0])

        if len(args.tokens) > 1:
            path = os.path.join(path, args.tokens[1])

        if len(args.tokens) > 2:
            user = args.tokens[2]
            user_dir = f"user/work.{user}"
            candidate = os.path.join(path, user_dir)
            if os.path.exists(candidate):
                path = candidate

    print(path)


if __name__ == "__main__":
    main()

