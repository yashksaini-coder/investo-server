export class User {
    constructor(
        public readonly name: string,
        public readonly email: string,
        public readonly profilePicture: string, 
        public readonly password: string,
        public readonly id?: number
    ) {}
}
