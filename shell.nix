{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  propagatedBuildInputs = with pkgs; [
    (python38.withPackages (ps: with ps; [
      pynvim
      flake8
      black
      graphviz
      python-language-server
    ]))
  ];
}
