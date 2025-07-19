from odoo import http


class Hospital(http.Controller):
    @http.route('/member_webform', type='http', auth='user', website=True)
    def member_webform(self, **kw):
        return http.request.render('mentors_bonus_penalty.create_member', {})

    @http.route('/create/webmember', type='http', auth='user', website=True)
    def create_webmember(self, **kw):
        http.request.env['res.partner'].sudo().create(kw)
        return http.request.render('member_thanks', {})
