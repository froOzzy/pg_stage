{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [ pkgs.python311 ];

  shellHook = ''
    if [ ! -d .venv ]; then
      ${pkgs.python311}/bin/python3 -m venv .venv
      .venv/bin/python -m pip install -e . \
        pytest==7.3.1 bandit==1.7.5 ruff==0.11.8 mypy==1.4.1
    fi

    if [ ! -x .venv/bin/python ]; then
      echo "The .venv interpreter is unavailable. Recreate .venv inside nix-shell."
      return 1
    fi

    source .venv/bin/activate
  '';
}
