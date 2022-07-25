let
  pkgs = import <nixpkgs> { };
in
with pkgs;
let
  pythonWithPackages = python3.withPackages (
    ps: with ps; [
      black
      flake8
      graphviz
      numpy
      pynvim
      z3
    ]
  );
  binName = "python";

  PROJECT_ROOT = builtins.getEnv "PWD";

  curl = ''${pkgs.curl}/bin/curl -f --cookie "session=$sessionToken"'';
  rg = "${ripgrep}/bin/rg --color never";

  noSessionToken = ''
    echo -e "\033[0;31m.---------------------------.\033[0m"
    echo -e "\033[0;31m|                           |\033[0m"
    echo -e "\033[0;31m| Session Token is not set! |\033[0m"
    echo -e "\033[0;31m|                           |\033[0m"
    echo -e "\033[0;31m'---------------------------'\033[0m"
    exit 1
  '';

  getInputScript = writeShellScriptBin "getinput" ''
    [[ $1 == "" ]] && echo "Usage: getinput <day>" && exit 1
    year=$(basename $(pwd))

    # Error if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && echo "Not a year dir" && exit 1

    outfile=$1
    [[ $(echo "$1 < 10" | ${bc}/bin/bc) == "1" ]] && outfile="0$outfile"

    [[ -f inputs/$outfile.txt ]] && less inputs/$outfile.txt && exit 0

    mkdir -p inputs
    if [[ -f ${PROJECT_ROOT}/.session_token ]]; then
      sessionToken=$(cat ${PROJECT_ROOT}/.session_token)
      ${curl} --output inputs/$outfile.txt https://adventofcode.com/$year/day/$1/input
    else
      ${noSessionToken}
    fi

    less inputs/$outfile.txt
  '';

  printStatsScript = writeShellScriptBin "printstats" ''
    year=$(basename $(pwd))

    # Skip if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && exit 0

    if [[ -f ${PROJECT_ROOT}/.session_token ]]; then
      sessionToken=$(cat ${PROJECT_ROOT}/.session_token)
      ${curl} -s https://adventofcode.com/$year/leaderboard/self |
        ${html-xml-utils}/bin/hxselect -c pre |
        ${gnused}/bin/sed "s/<[^>]*>//g" |
        ${rg} "^\s*(Day\s+Time|-+Part|\d+\s+(&gt;24h|\d{2}:\d{2}:\d{2}))" |
        ${gnused}/bin/sed "s/&gt;/>/g"
    else
      ${noSessionToken}
    fi
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

    ${watchexec}/bin/watchexec -r "${pythonWithPackages}/bin/${binName} ./$day.py"
  '';

  debugRunScript = writeShellScriptBin "drun" ''
    ${getDayScriptPart "drun"}

    ${watchexec}/bin/watchexec -r "${pythonWithPackages}/bin/${binName} ./$day.py --debug"
  '';

  # Single run, don't watchexec
  singleRunScript = writeShellScriptBin "srun" ''
    ${getDayScriptPart "srun"}

    ${pythonWithPackages}/bin/${binName} ./$day.py
  '';

  debugSingleRunScript = writeShellScriptBin "dsrun" ''
    ${getDayScriptPart "dsrun"}

    ${pythonWithPackages}/bin/${binName} ./$day.py --debug
  '';

  # Write a test file
  mkTestScript = writeShellScriptBin "mktest" ''
    ${getDayScriptPart "mktest"}
    if [[ -z "$WAYLAND_DISPLAY" ]]; then
      ${xsel}/bin/xsel --output > inputs/$day.test.txt
    else
      ${wl-clipboard}/bin/wl-paste -p > inputs/$day.test.txt
    fi
  '';

  # Run with --notest flag
  runNoTestScript = writeShellScriptBin "rntest" ''
    ${getDayScriptPart "rntest"}
    ${pythonWithPackages}/bin/${binName} ./$day.py --notest
  '';

  debugRunNoTestScript = writeShellScriptBin "drntest" ''
    ${getDayScriptPart "druntest"}
    ${pythonWithPackages}/bin/${binName} ./$day.py --notest --debug
  '';

  # Run with --stdin and --notest flags
  runStdinScript = writeShellScriptBin "runstdin" ''
    ${getDayScriptPart "runstdin"}
    ${pythonWithPackages}/bin/${binName} ./$day.py --stdin --notest
  '';

  # Run with --stdin and --notest flags, and pull from clipboard.
  runStdinClipScript = writeShellScriptBin "runstdinclip" ''
    ${getDayScriptPart "runstdin"}
    ${xsel}/bin/xsel --output | ${pythonWithPackages}/bin/${binName} ./$day.py --stdin --notest
  '';

  # Compile and run the C version.
  cRunScript = writeShellScriptBin "crun" ''
    ${getDayScriptPart "crun"}
    mkdir -p bin
    gcc -o bin/$day $day.c
    ./bin/$day <inputs/$day.txt
  '';

  cRunTestScript = writeShellScriptBin "cruntest" ''
    ${getDayScriptPart "cruntest"}
    mkdir -p bin
    gcc -o bin/$day $day.c
    ./bin/$day --test <inputs/$day.txt
  '';

  # CoC Config
  cocConfig = writeText "coc-settings.json" (
    builtins.toJSON {
      "python.formatting.provider" = "black";
      "python.linting.flake8Enabled" = true;
      "python.linting.mypyEnabled" = true;
      "python.linting.pylintEnabled" = false;
      "python.pythonPath" = "${pythonWithPackages}/bin/${binName}";
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

    # Golang
    go
    gopls
    gotools

    # OCaml
    ocaml
    ocamlformat
    ocamlPackages.ocaml-lsp
    ocamlPackages.ocaml_extlib
    ocamlPackages.utop

    # Python
    pythonWithPackages.pkgs.black
    pythonWithPackages.pkgs.flake8
    pythonWithPackages
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
