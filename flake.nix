{
  description = "Advent of Code environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonWithPackages = pkgs.python3.withPackages
          (ps: with ps; [ black flake8 graphviz numpy pynvim z3-solver ]);
        binName = "python";

        curl = ''${pkgs.curl}/bin/curl -f --cookie "session=$sessionToken"'';
        rg = "${pkgs.ripgrep}/bin/rg --color never";

        noSessionToken = ''
          echo -e "\033[0;31m.---------------------------.\033[0m"
          echo -e "\033[0;31m|                           |\033[0m"
          echo -e "\033[0;31m| Session Token is not set! |\033[0m"
          echo -e "\033[0;31m|                           |\033[0m"
          echo -e "\033[0;31m'---------------------------'\033[0m"
          exit 1
        '';

        getDayScriptPart = scriptName: ''
          # Check that day is passed in.
          [[ $1 == "" ]] && echo "Usage: ${scriptName} <day>" && exit 1
          day=$1

          # Error if no day
          [[ ! $(echo $day | ${rg} "\d+") ]] && echo "Not a valid day" && exit 1

          # Zero-pad day
          [[ $(echo "$1 < 10" | ${pkgs.bc}/bin/bc) == "1" ]] && day="0$day"
        '';

        initDayScript = pkgs.writeShellScriptBin "initday" ''
          yearDirname=$(basename $(pwd))

          # Error if not a year dir
          [[ ! $(echo $yearDirname | ${rg} "y\d{4}") ]] && echo "Not a year dir" && exit 1
          year=''${yearDirname:1}

          ${getDayScriptPart "initday"}

          mkdir -p $PROJECT_ROOT/$yearDirname/d$day
          touch $PROJECT_ROOT/$yearDirname/d$day/$day.test.1.txt
          cat $PROJECT_ROOT/templates/template.go \
            | sed "s/%DAYNUM%/$day/g" \
            > $PROJECT_ROOT/$yearDirname/d$day/$day.go
          cat $PROJECT_ROOT/templates/testtemplate.go \
            | sed "s/%DAYNUM%/$day/g" \
            | sed "s/%YEARNUM%/$year/g" \
            > $PROJECT_ROOT/$yearDirname/d$day/''${day}_test.go

          cd $PROJECT_ROOT/$yearDirname/d$day
        '';

        getInputScript = pkgs.writeShellScriptBin "getinput" ''
          dayDirname=$(basename $(pwd))

          # Error if not a solution dir
          [[ ! $(echo $dayDirname | ${rg} "d\d{2}") ]] && echo "Not a day solution dir" && exit 1
          day=''${dayDirname:1}

          yearDirname=$(basename $(dirname $(pwd)))

          # Error if not a year dir
          [[ ! $(echo $yearDirname | ${rg} "y\d{4}") ]] && echo "Not a year dir" && exit 1
          year=''${yearDirname:1}

          [[ -f $day.txt ]] && less $day.txt && exit 0

          if [[ -f $PROJECT_ROOT/.session_token ]]; then
            dayTruncated=$day
            [[ $(echo "$day < 10" | ${pkgs.bc}/bin/bc) == "1" ]] && dayTruncated=''${day:1}
            sessionToken=$(cat $PROJECT_ROOT/.session_token)
            ${curl} --output $day.txt https://adventofcode.com/$year/day/$dayTruncated/input
          else
            ${noSessionToken}
          fi

          less $day.txt
        '';

        printStatsScript = pkgs.writeShellScriptBin "printstats" ''
          yearDirname=$(basename $(pwd))

          # Skip if not a year dir
          [[ ! $(echo $yearDirname | ${rg} "y\d{4}") ]] && exit 0
          year=''${yearDirname:1}

          if [[ -f $PROJECT_ROOT/.session_token ]]; then
            sessionToken=$(cat $PROJECT_ROOT/.session_token)
            ${curl} -s https://adventofcode.com/$year/leaderboard/self |
              ${pkgs.html-xml-utils}/bin/hxselect -c pre |
              ${pkgs.gnused}/bin/sed "s/<[^>]*>//g" |
              ${rg} "^\s*(Day\s+Time|-+Part|\d+\s+(&gt;24h|\d{2}:\d{2}:\d{2}))" |
              ${pkgs.gnused}/bin/sed "s/&gt;/>/g"
          else
            ${noSessionToken}
          fi
        '';

        runScript = pkgs.writeShellScriptBin "run" ''
          ${getDayScriptPart "run"}

          ${pkgs.watchexec}/bin/watchexec -r "${pythonWithPackages}/bin/${binName} ./$day.py"
        '';

        debugRunScript = pkgs.writeShellScriptBin "drun" ''
          ${getDayScriptPart "drun"}

          ${pkgs.watchexec}/bin/watchexec -r "${pythonWithPackages}/bin/${binName} ./$day.py --debug"
        '';

        # Single run, don't watchexec
        singleRunScript = pkgs.writeShellScriptBin "srun" ''
          ${getDayScriptPart "srun"}

          ${pythonWithPackages}/bin/${binName} ./$day.py
        '';

        debugSingleRunScript = pkgs.writeShellScriptBin "dsrun" ''
          ${getDayScriptPart "dsrun"}

          ${pythonWithPackages}/bin/${binName} ./$day.py --debug
        '';

        # Write a test file
        mkTestScript = pkgs.writeShellScriptBin "mktest" ''
          ${getDayScriptPart "mktest"}
          if [[ -z "$WAYLAND_DISPLAY" ]]; then
            ${pkgs.xsel}/bin/xsel --output > inputs/$day.test.txt
          else
            ${pkgs.wl-clipboard}/bin/wl-paste -p > inputs/$day.test.txt
          fi
        '';

        # Run with --notest flag
        runNoTestScript = pkgs.writeShellScriptBin "rntest" ''
          ${getDayScriptPart "rntest"}
          ${pythonWithPackages}/bin/${binName} ./$day.py --notest
        '';

        debugRunNoTestScript = pkgs.writeShellScriptBin "drntest" ''
          ${getDayScriptPart "druntest"}
          ${pythonWithPackages}/bin/${binName} ./$day.py --notest --debug
        '';

        # Run with --stdin and --notest flags
        runStdinScript = pkgs.writeShellScriptBin "runstdin" ''
          ${getDayScriptPart "runstdin"}
          ${pythonWithPackages}/bin/${binName} ./$day.py --stdin --notest
        '';

        # Run with --stdin and --notest flags, and pull from clipboard.
        runStdinClipScript = pkgs.writeShellScriptBin "runstdinclip" ''
          ${getDayScriptPart "runstdin"}
          ${pkgs.xsel}/bin/xsel --output | ${pythonWithPackages}/bin/${binName} ./$day.py --stdin --notest
        '';

        # Compile and run the C version.
        cRunScript = pkgs.writeShellScriptBin "crun" ''
          ${getDayScriptPart "crun"}
          mkdir -p bin
          gcc -o bin/$day $day.c
          ./bin/$day <inputs/$day.txt
        '';

        cRunTestScript = pkgs.writeShellScriptBin "cruntest" ''
          ${getDayScriptPart "cruntest"}
          mkdir -p bin
          gcc -o bin/$day $day.c
          ./bin/$day --test <inputs/$day.txt
        '';

        twitchChatScript = pkgs.writeShellScriptBin "twitchchat" ''
          TOKEN=$(cat $PROJECT_ROOT/.chat_token) 
          ttchat --channel sumnerevans --token $TOKEN
        '';
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Core
            coreutils
            gnumake
            tokei

            # Streaming
            twitchChatScript

            # C/C++
            clang
            gcc
            gdb
            valgrind

            # F#/C#
            dotnet-sdk
            # fsautocomplete

            # Golang
            go
            gopls
            gotools

            # Kotlin
            gradle
            kotlin

            # OCaml
            ocaml
            ocamlformat
            ocamlPackages.ocaml-lsp
            ocamlPackages.extlib
            ocamlPackages.utop

            # Python
            pythonWithPackages.pkgs.black
            pythonWithPackages.pkgs.flake8
            pythonWithPackages
            pypy3

            # Typescript
            typescript

            # Utilities
            initDayScript
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
        };
      }));
}
