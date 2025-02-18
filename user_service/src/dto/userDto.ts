import { IsNotEmpty, IsString, IsEmail, MinLength } from 'class-validator';

export class CreateUserRequest {

    @IsNotEmpty()
    @IsString()
    name: string;
  
    @IsNotEmpty()
    @IsEmail()
    email: string;
  
    @IsNotEmpty()
    @IsString()
    password: string;
    @IsString()
    profilePicture?: string;
  }
  



export class UpdateUserRequest {
  @IsNotEmpty()
  @IsString()
  name?: string;
  @IsNotEmpty()
  @IsEmail()
  email?: string;
  @IsNotEmpty()
  @IsString()
  password?: string;
  @IsString()
  profilePicture?: string;
}
export class LoginRequest {
  @IsNotEmpty()
  @IsString()
  email: string;
  @IsNotEmpty()
  @IsString()
  password: string;
}