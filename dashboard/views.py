from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import LoanProfile

def home(request):
    return render(request, "dashboard.html")

def search_suggest(request):
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 1:
        profiles = LoanProfile.objects.filter(
            Q(name__icontains=q) | Q(email__icontains=q) |
            Q(code__icontains=q) | Q(status__icontains=q) |
            Q(score__icontains=q)
        )[:6]
        for p in profiles:
            results.append({'code': p.code, 'name': p.name,
                            'email': p.email, 'score': p.score, 'status': p.status})
    return JsonResponse({'results': results})

def profile_list_view(request):
    status_filter = request.GET.get('status', 'all')
    search_query  = request.GET.get('q', '').strip()
    sort_order    = request.GET.get('sort', '')
    if status_filter == 'approved':
        queryset = LoanProfile.objects.filter(status='Đã duyệt')
    elif status_filter == 'pending':
        queryset = LoanProfile.objects.filter(status='Chờ xử lý')
    elif status_filter == 'rejected':
        queryset = LoanProfile.objects.filter(status='Từ chối')
    else:
        queryset = LoanProfile.objects.all()
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query) |
            Q(code__icontains=search_query) | Q(status__icontains=search_query) |
            Q(score__icontains=search_query)
        )
    if sort_order == 'score_desc':
        queryset = queryset.order_by('-score')
    elif sort_order == 'score_asc':
        queryset = queryset.order_by('score')
    paginator   = Paginator(queryset, 8)
    page_obj    = paginator.get_page(request.GET.get('page', 1))
    counts = {
        'all':      LoanProfile.objects.count(),
        'approved': LoanProfile.objects.filter(status='Đã duyệt').count(),
        'pending':  LoanProfile.objects.filter(status='Chờ xử lý').count(),
        'rejected': LoanProfile.objects.filter(status='Từ chối').count(),
    }
    return render(request, 'profile_list.html', {
        'profiles': page_obj, 'page_obj': page_obj, 'paginator': paginator,
        'status_filter': status_filter, 'search_query': search_query,
        'sort_order': sort_order, 'counts': counts,
    })

def score_result_view(request, pk):
    profile = get_object_or_404(LoanProfile, pk=pk)
    return render(request, 'score_result.html', {'profile': profile})

def score_detail_view(request, pk):
    profile = get_object_or_404(LoanProfile, pk=pk)
    base_score = 500
    factors = []

    avg_income = 35_000_000
    income_diff = int((float(profile.income) - avg_income) / avg_income * 100)
    income_pts = min(max(int((float(profile.income) - avg_income) / 1_000_000 * 5), -80), 150)
    factors.append({
        'label': 'Thu nhập ổn định cao' if income_pts > 0 else 'Thu nhập thấp hơn trung bình',
        'points': income_pts,
        'desc': f'Thu nhập {int(float(profile.income)//1_000_000)} triệu/tháng {"vượt" if income_diff > 0 else "thấp hơn"} trung bình {abs(income_diff)}% so với nhóm tương tự',
        'type': 'positive' if income_pts > 0 else 'negative',
    })

    work_pts = min(profile.work_years * 18, 110)
    factors.append({
        'label': 'Thời gian làm việc dài' if work_pts > 40 else 'Thời gian làm việc ngắn',
        'points': work_pts,
        'desc': f'{profile.work_years} năm kinh nghiệm tại công ty cho thấy {"sự ổn định nghề nghiệp" if work_pts > 40 else "cần thêm thời gian"}',
        'type': 'positive' if work_pts > 40 else 'neutral',
    })

    if profile.late_payments == 0:
        factors.append({'label': 'Lịch sử thanh toán tốt', 'points': 80,
            'desc': 'Không có khoản nợ quá hạn trong 24 tháng qua', 'type': 'positive'})
    elif profile.late_payments <= 2:
        factors.append({'label': 'Có một vài lần trễ hạn', 'points': -20,
            'desc': f'{profile.late_payments} lần trễ hạn trong 24 tháng qua', 'type': 'negative'})
    else:
        factors.append({'label': 'Lịch sử thanh toán kém', 'points': -80,
            'desc': f'{profile.late_payments} lần trễ hạn — rủi ro cao', 'type': 'negative'})

    if profile.debt_ratio <= 25:
        factors.append({'label': 'Tỷ lệ nợ trên thu nhập tốt', 'points': 30,
            'desc': f'Nợ chiếm {profile.debt_ratio}% thu nhập, nằm trong ngưỡng an toàn', 'type': 'positive'})
    elif profile.debt_ratio <= 40:
        factors.append({'label': 'Tỷ lệ nợ trên thu nhập cao', 'points': -45,
            'desc': f'Nợ chiếm {profile.debt_ratio}% thu nhập, cao hơn mức khuyến nghị 25%', 'type': 'negative'})
    else:
        factors.append({'label': 'Tỷ lệ nợ quá cao', 'points': -90,
            'desc': f'Nợ chiếm {profile.debt_ratio}% thu nhập — vượt ngưỡng an toàn', 'type': 'negative'})

    if profile.active_loans == 0:
        factors.append({'label': 'Không có khoản vay hiện tại', 'points': 20,
            'desc': 'Không có khoản vay đang hoạt động', 'type': 'positive'})
    elif profile.active_loans <= 2:
        factors.append({'label': 'Số lượng khoản vay vừa phải', 'points': -20,
            'desc': f'Có {profile.active_loans} khoản vay đang hoạt động', 'type': 'neutral'})
    else:
        factors.append({'label': 'Nhiều khoản vay cùng lúc', 'points': -35,
            'desc': f'Hiện có {profile.active_loans} khoản vay, cao hơn mức trung bình', 'type': 'negative'})

    total_plus  = sum(f['points'] for f in factors if f['points'] > 0)
    total_minus = sum(f['points'] for f in factors if f['points'] < 0)

    return render(request, 'score_detail.html', {
        'profile': profile, 'factors': factors,
        'base_score': base_score, 'total_plus': total_plus, 'total_minus': total_minus,
    })