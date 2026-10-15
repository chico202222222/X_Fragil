import DTO from './dto.js';
import { validarLogin, validarRegistro } from './validacaoCampos.js';

class RegisterMiddleware {
  static validateRegisterMiddleware(req, res, next) {
    const result = validarRegistro(req.body);
    if (result.error) return res.status(400).json({ error: result.error });
    req.authData = result.data;
    next();
  }

  static async createUserMiddleware(req, res, next) {
    try {
      const exists = await DTO.verifyUser({ email: req.authData.email });
      if (exists) return res.status(409).json({ error: 'Usuário já existe' });
      req.user = await DTO.createUser(req.authData);
      next();
    } catch {
      return res.status(500).json({ error: 'Erro ao criar usuário' });
    }
  }
}

class LoginMiddleware {
  static validateLoginMiddleware(req, res, next) {
    const result = validarLogin(req.body);
    if (result.error) return res.status(400).json({ error: result.error });
    req.authData = result.data;
    next();
  }

  static async createLoginMiddleware(req, res, next) {
    try {
      const user = await DTO.loginUser(req.authData);
      if (!user) return res.status(401).json({ error: 'Usuário ou senha inválidos' });
      req.user = user;
      next();
    } catch {
      return res.status(500).json({ error: 'Erro ao fazer login' });
    }
  }
}

export { RegisterMiddleware, LoginMiddleware };
