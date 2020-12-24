let
  pkgs = import <nixpkgs> {};
  py3WithPackages = pkgs.python3.withPackages (
    ps: with ps; [
      black
      flake8
      graphviz
      pynvim
      python-language-server
    ]
  );

  sessionToken = pkgs.lib.removeSuffix "\n" (builtins.readFile ./.session_token);
  curl = ''${pkgs.curl}/bin/curl -f --cookie "session=${sessionToken}"'';
  rg = "${pkgs.ripgrep}/bin/rg --color never";
  getInputScript = pkgs.writeShellScriptBin "getinput" ''
    [[ $1 == "" ]] && echo "Usage: getinput <day>" && exit 1
    year=$(basename $(pwd))

    # Error if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && echo "Not a year dir" && exit 1

    outfile=$1
    [[ $(echo "$1 < 10" | bc) == "1" ]] && outfile="0$outfile"

    mkdir -p inputs
    ${curl} --output inputs/$outfile.txt https://adventofcode.com/$year/day/$1/input

    less inputs/$outfile.txt
  '';

  printStatsScript = pkgs.writeShellScriptBin "printstats" ''
    year=$(basename $(pwd))

    # Skip if not a year dir
    [[ ! $(echo $year | ${rg} "\d{4}") ]] && exit 0

    ${curl} -s https://adventofcode.com/$year/leaderboard/self |
      ${pkgs.html-xml-utils}/bin/hxselect -c pre |
      ${pkgs.gnused}/bin/sed "s/<[^>]*>//g" |
      ${rg} "^\s*(Day\s+Time|-+Part|\d+\s+(&gt;24h|\d{2}:\d{2}:\d{2}))" |
      ${pkgs.gnused}/bin/sed "s/&gt;/>/g"
  '';

  getDayScriptPart = scriptName: ''
    # Check that day is passed in.
    [[ $1 == "" ]] && echo "Usage: ${scriptName} <day>" && exit 1
    day=$1

    # Error if no day
    [[ ! $(echo $day | ${rg} "\d+") ]] && echo "Not a valid day" && exit 1

    # Zero-pad day
    [[ $(echo "$1 < 10" | bc) == "1" ]] && day="0$day"
  '';

  runScript = pkgs.writeShellScriptBin "run" ''
    ${getDayScriptPart "run"}

    ${pkgs.watchexec}/bin/watchexec -r "${pkgs.pypy3}/bin/pypy3 ./$day.py <./inputs/$day.txt"
  '';

  debugRunScript = pkgs.writeShellScriptBin "drun" ''
    ${getDayScriptPart "drun"}

    ${pkgs.watchexec}/bin/watchexec -r "${pkgs.pypy3}/bin/pypy3 ./$day.py --debug <./inputs/$day.txt"
  '';

  # Single run, don't watchexec
  singleRunScript = pkgs.writeShellScriptBin "srun" ''
    ${getDayScriptPart "srun"}

    ${pkgs.pypy3}/bin/pypy3 ./$day.py <./inputs/$day.txt
  '';

  debugSingleRunTestScript = pkgs.writeShellScriptBin "dsrun" ''
    ${getDayScriptPart "dsrun"}

    ${pkgs.pypy3}/bin/pypy3 ./$day.py --debug <./inputs/$day.txt
  '';

  # Write a test file
  mkTestScript = pkgs.writeShellScriptBin "mktest" ''
    ${getDayScriptPart "mktest"}
    ${pkgs.xsel}/bin/xsel --output > inputs/$day.test.txt
  '';

  runTestScript = pkgs.writeShellScriptBin "runtest" ''
    ${getDayScriptPart "runtest"}
    ${pkgs.pypy3}/bin/pypy3 ./$day.py --test <./inputs/$day.test.txt
  '';

  debugRunTestScript = pkgs.writeShellScriptBin "druntest" ''
    ${getDayScriptPart "druntest"}
    ${pkgs.pypy3}/bin/pypy3 ./$day.py --test --debug <./inputs/$day.test.txt
  '';

  cRunScript = pkgs.writeShellScriptBin "crun" ''
    ${getDayScriptPart "crun"}
    mkdir -p bin
    gcc -o bin/$day $day.c
    ./bin/$day <./inputs/$day.txt
  '';

  cRunTestScript = pkgs.writeShellScriptBin "cruntest" ''
    ${getDayScriptPart "cruntest"}
    mkdir -p bin
    gcc -o bin/$day $day.c
    ./bin/$day <./inputs/$day.test.txt
  '';

  # CoC Config
  cocConfig = pkgs.writeText "coc-settings.json" (
    builtins.toJSON {
      "python.formatting.provider" = "black";
      "python.linting.flake8Enabled" = true;
      "python.linting.mypyEnabled" = true;
      "python.linting.pylintEnabled" = false;
      "python.pythonPath" = "${py3WithPackages}/bin/python";
      "clangd.path" = "${pkgs.clang-tools}/bin/clangd";
    }
  );
in
pkgs.mkShell {
  shellHook = ''
    mkdir -p .vim
    ln -sf ${cocConfig} .vim/coc-settings.json
  '';

  POST_CD_COMMAND = "${printStatsScript}/bin/printstats";

  buildInputs = with pkgs; [
    # Core
    coreutils
    gnumake
    rnix-lsp

    # C/C++
    clang
    gcc
    gdb
    valgrind

    # Python
    py3WithPackages
    py3WithPackages.pkgs.black
    py3WithPackages.pkgs.flake8
    pypy3

    # Utilities
    cRunScript
    cRunTestScript
    debugRunScript
    debugRunTestScript
    debugSingleRunTestScript
    getInputScript
    mkTestScript
    printStatsScript
    runScript
    runTestScript
    singleRunScript
  ];
}
