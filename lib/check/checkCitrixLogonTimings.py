from .base import Base

# https://www.citrix.com/blogs/2014/05/30/wmi-objects-used-by-citrix-director-for-troubleshooting-sessions-2/


class CheckCitrixLogonTimings(Base):

    qry = '''
    SELECT
    GroupPolicyComplete, GroupPolicyStart, ProfileLoaded, ProfileLoadStart,
    LogonScriptsComplete, LogonScriptsStart
    FROM LogonTimings
    '''
    type_name = 'session'
    namespace = 'root/citrix/profiles/metrics'

    @classmethod
    def iterate_results(cls, wmi_data):
        session = {
            'sessionCount': len(wmi_data),
            'name': 'session'
        }

        grouppolicy_timings = []
        profileload_timings = []
        logonscripts_timings = []
        for itm in wmi_data:
            try:
                td = itm['GroupPolicyComplete'] - itm['GroupPolicyStart']
                grouppolicy_timings.append(td.seconds)
            except Exception:
                pass

            try:
                td = itm['ProfileLoaded'] - itm['ProfileLoadStart']
                profileload_timings.append(td.seconds)
            except Exception:
                pass

            try:
                td = itm['LogonScriptsComplete'] - itm['LogonScriptsStart']
                logonscripts_timings.append(td.seconds)
            except Exception:
                pass

        for name, lst in (
                ('GroupPolicyTiming', grouppolicy_timings),
                ('ProfileLoadTiming', profileload_timings),
                ('LogonScriptsTiming', logonscripts_timings)):
            n = len(lst)
            if n:
                session[name + 'Min'] = min(lst)
                session[name + 'Max'] = max(lst)
                session[name + 'Avg'] = sum(lst) / n
                session[name + 'Jitter'] = \
                    sum(abs(a - b) for a, b in zip(lst[1:], lst)) / (n - 1) \
                    if n > 1 else None

        return {
            cls.type_name: [session]
        }
