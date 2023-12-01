import * as readline from 'readline';

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const lines: string[] = [];

rl.on('line', (line: string) => {
    lines.push(line);
}).on('close', () => {
    console.log('Part 1')
    console.log(lines.map((line: string) => {
        const ints = line.split('').filter((char: string) => /^\d+$/.test(char))
        return parseInt(ints[0] + ints[ints.length - 1])
    }).reduce((acc: number, cur: number) => acc + cur, 0))

    console.log('Part 2')
    console.log(lines.map((line: string) => {
        const ints: number[] = []
        for (let i = 0; i < line.length; i++) {
            const part = line.substring(i)
            if (/^\d+$/.test(line[i])) {
                ints.push(parseInt(line[i]))
            } else if (part.startsWith('one')) {
                ints.push(1)
            } else if (part.startsWith('two')) {
                ints.push(2)
            } else if (part.startsWith('three')) {
                ints.push(3)
            } else if (part.startsWith('four')) {
                ints.push(4)
            } else if (part.startsWith('five')) {
                ints.push(5)
            } else if (part.startsWith('six')) {
                ints.push(6)
            } else if (part.startsWith('seven')) {
                ints.push(7)
            } else if (part.startsWith('eight')) {
                ints.push(8)
            } else if (part.startsWith('nine')) {
                ints.push(9)
            }
        }
        return parseInt('' + ints[0] + ints[ints.length - 1])
    }).reduce((acc: number, cur: number) => acc + cur, 0))
})
