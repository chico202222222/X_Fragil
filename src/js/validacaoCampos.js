// deprecado, html tem validacao nativa, mas é bom deixar aqui
import { z } from 'zod';

export function dadosDoForm(form) {
  return Object.fromEntries(new FormData(form));
}

const loginSchema = z.object({
  email: z.string().min(4).max(255).email('Email inválido'),
  senha: z
    .string()
    .min(8, 'Senha precisa ter entre 8 e 255 caracteres')
    .max(255, 'Senha precisa ter entre 8 e 255 caracteres'),
});

const registerSchema = z
  .object({
    nome: z // nome do usuário (id: nome)
      .string()
      .min(4, 'Nome precisa ter entre 4 e 255 caracteres')
      .max(255, 'Nome precisa ter entre 4 e 255 caracteres'),
    email: z.string().min(4).max(255).email('Email inválido'),
    senha: z
      .string()
      .min(8, 'Senha precisa ter entre 8 e 255 caracteres')
      .max(255, 'Senha precisa ter entre 8 e 255 caracteres'),
    confirmarSenha: z.string().min(8).max(255),
  })
  .refine((d) => d.senha === d.confirmarSenha, {
    message: 'Senhas não conferem',
    path: ['confirmarSenha'],
  });

function validar(schema, dados) {
  const result = schema.safeParse(dados ?? {});
  if (!result.success) {
    return { error: result.error.issues[0].message };
  }
  return { success: true, data: result.data };
}

export function validarLogin(dados) {
  return validar(loginSchema, dados);
}

export function validarRegistro(dados) {
  const out = validar(registerSchema, dados);
  if (out.error) return out;
  const { confirmarSenha, ...data } = out.data;
  return { success: true, data };
}

export function validateLogin(form) {
  return validarLogin(dadosDoForm(form));
}

export function validateRegister(form) {
  return validarRegistro(dadosDoForm(form));
}
