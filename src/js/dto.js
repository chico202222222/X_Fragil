import prisma from '../prisma/prisma.js';
// puxa a info da database (wip, sem database)
class DTO {
  static async createUser(data) {
    return prisma.user.create({
      data: {
        nome: data.nome,
        email: data.email,
        senha: data.senha,
      },
    });
  }

  static async loginUser(data) {
    return prisma.user.findFirst({
      where: {
        email: data.email,
        senha: data.senha,
      },
    });
  }

  static async verifyUser(data) {
    return prisma.user.findUnique({
      where: { email: data.email },
    });
  }
}

export default DTO;

export async function loginUser(data) {
  return DTO.loginUser(data);
}

export async function createUser(data) {
  return DTO.createUser(data);
}
