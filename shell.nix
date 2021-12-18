let
  pkgs = import <nixpkgs> { };
in
with pkgs;
let
  py3WithPackages = python3.withPackages (
    ps: with ps; [
      black
      flake8
      graphviz
      pynvim
    ]
  );

  PROJECT_ROOT = builtins.getEnv "PWD";

  curl = ''${pkgs.curl}/bin/curl -f --cookie "session=$sessionToken"'';
  rg = "${ripgrep}/bin/rg --color never";
  getInputScript = writeShellScriptBin "getinput" ''
    [[ $1 == "" ]] && echo "Usage: getinput <day>" && exit 1
    year=$(basename $(pwd))

    # Error if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && echo "Not a year dir" && exit 1

    outfile=$1
    [[ $(echo "$1 < 10" | ${bc}/bin/bc) == "1" ]] && outfile="0$outfile"

    [[ -f inputs/$outfile.txt ]] && less inputs/$outfile.txt && exit 0

    mkdir -p inputs
    sessionToken=$(cat ${PROJECT_ROOT}/.session_token)
    ${curl} --output inputs/$outfile.txt https://adventofcode.com/$year/day/$1/input

    less inputs/$outfile.txt
  '';

  printStatsScript = writeShellScriptBin "printstats" ''
    year=$(basename $(pwd))

    # Skip if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && exit 0

    sessionToken=$(cat ${PROJECT_ROOT}/.session_token)
    ${curl} -s https://adventofcode.com/$year/leaderboard/self |
      ${html-xml-utils}/bin/hxselect -c pre |
      ${gnused}/bin/sed "s/<[^>]*>//g" |
      ${rg} "^\s*(Day\s+Time|-+Part|\d+\s+(&gt;24h|\d{2}:\d{2}:\d{2}))" |
      ${gnused}/bin/sed "s/&gt;/>/g"
  '';

  getDayScriptPart = scriptName: ''
    # Check that day is passed in.
    [[ $1 == "" ]] && echo "Usage: ${scriptName} <day>" && exit 1
    day=$1

    # Error if no day
    [[ ! $(echo $day | ${rg} "\d+") ]] && echo "Not a valid day" && exit 1

    # Zero-pad day
    [[ $(echo "$1 < 10" | ${bc}/bin/bc) == "1" ]] && day="0$day"
  '';

  runScript = writeShellScriptBin "run" ''
    ${getDayScriptPart "run"}

    ${watchexec}/bin/watchexec -r "${pypy3}/bin/pypy3 ./$day.py"
  '';

  debugRunScript = writeShellScriptBin "drun" ''
    ${getDayScriptPart "drun"}

    ${watchexec}/bin/watchexec -r "${pypy3}/bin/pypy3 ./$day.py --debug"
  '';

  # Single run, don't watchexec
  singleRunScript = writeShellScriptBin "srun" ''
    ${getDayScriptPart "srun"}

    ${pypy3}/bin/pypy3 ./$day.py
  '';

  debugSingleRunScript = writeShellScriptBin "dsrun" ''
    ${getDayScriptPart "dsrun"}

    ${pypy3}/bin/pypy3 ./$day.py --debug
  '';

  # Write a test file
  mkTestScript = writeShellScriptBin "mktest" ''
    ${getDayScriptPart "mktest"}
    # TODO detect wayland vs xorg
    ${wl-clipboard}/bin/wl-paste -p > inputs/$day.test.txt
  '';

  # Run with --notest flag
  runNoTestScript = writeShellScriptBin "rntest" ''
    ${getDayScriptPart "rntest"}
    ${pypy3}/bin/pypy3 ./$day.py --notest
  '';

  debugRunNoTestScript = writeShellScriptBin "drntest" ''
    ${getDayScriptPart "druntest"}
    ${pypy3}/bin/pypy3 ./$day.py --notest --debug
  '';

  # Run with --stdin and --notest flags
  runStdinScript = writeShellScriptBin "runstdin" ''
    ${getDayScriptPart "runstdin"}
    ${pypy3}/bin/pypy3 ./$day.py --stdin --notest
  '';

  # Run with --stdin and --notest flags, and pull from clipboard.
  runStdinClipScript = writeShellScriptBin "runstdinclip" ''
    ${getDayScriptPart "runstdin"}
    ${xsel}/bin/xsel --output | ${pypy3}/bin/pypy3 ./$day.py --stdin --notest
  '';

  # Compile and run the C version.
  cRunScript = writeShellScriptBin "crun" ''
    ${getDayScriptPart "crun"}
    mkdir -p bin
    gcc -o bin/$day $day.c
    ./bin/$day
  '';

  cRunTestScript = writeShellScriptBin "cruntest" ''
    ${getDayScriptPart "cruntest"}
    mkdir -p bin
    gcc -o bin/$day $day.c
    ./bin/$day --test
  '';

  # CoC Config
  cocConfig = writeText "coc-settings.json" (
    builtins.toJSON {
      "python.formatting.provider" = "black";
      "python.linting.flake8Enabled" = true;
      "python.linting.mypyEnabled" = true;
      "python.linting.pylintEnabled" = false;
      "python.pythonPath" = "${py3WithPackages}/bin/python";
      "clangd.path" = "${clang-tools}/bin/clangd";
      "languageserver" = {
        "ocaml-lsp" = {
          command = "${ocamlPackages.ocaml-lsp}/bin/ocamllsp";
          filetypes = [ "ocaml" "reason" ];
        };
      };
    }
  );
in
mkShell {
  shellHook = ''
    mkdir -p .vim
    ln -sf ${cocConfig} ${PROJECT_ROOT}/.vim/coc-settings.json
  '';

  POST_CD_COMMAND = "${printStatsScript}/bin/printstats";

  buildInputs = [
    # Core
    coreutils
    gnumake
    rnix-lsp
    sloccount
    tokei

    # C/C++
    clang
    gcc
    gdb
    valgrind

    # OCaml
    ocaml
    ocamlformat
    ocamlPackages.ocaml-lsp
    ocamlPackages.ocaml_extlib
    ocamlPackages.utop

    # Python
    py3WithPackages
    py3WithPackages.pkgs.black
    py3WithPackages.pkgs.flake8
    pypy3

    # Utilities
    cRunScript
    cRunTestScript
    debugRunScript
    debugRunNoTestScript
    debugSingleRunScript
    getInputScript
    mkTestScript
    printStatsScript
    runScript
    runStdinClipScript
    runStdinScript
    runNoTestScript
    singleRunScript
  ];
}
