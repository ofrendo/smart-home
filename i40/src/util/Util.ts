import shajs from "sha.js";

export class Util {

    private static hashAlgorithm = shajs("sha256");

    static hash(input: string): string {
        return this.hashAlgorithm.update(input).digest("hex");
    }

}




